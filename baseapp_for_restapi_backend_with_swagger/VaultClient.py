import hvac
import datetime
import threading

DEFAULT_EXPIRY_DURATION = datetime.timedelta(minutes=5)

class VaultClient():
    client = None
    dependantRefs = None
    getCurDateTime = None
    VAULT_ROLE_ID = None
    VAULT_SECRET_ID = None

    def __init__(self, env, getReadFromEnviromentFn, getCurDateTime):
        print("Setting up vault")
        self._lock = threading.Lock()
        self.getCurDateTime = getCurDateTime
        self.dependantRefs = {}
        VAULT_URL = getReadFromEnviromentFn(
            env=env,
            envVarName="APIAPP_VAULT_URL",
            defaultValue=None,
            acceptableValues=None,
            nullValueAllowed=False,
            vaultClient=None
        )()
        print(" VAULT_URL:", VAULT_URL)
        self.VAULT_ROLE_ID = getReadFromEnviromentFn(
            env=env,
            envVarName="APIAPP_VAULT_ROLE_ID",
            defaultValue=None,
            acceptableValues=None,
            nullValueAllowed=False,
            vaultClient=None
        )()
        self.VAULT_SECRET_ID = getReadFromEnviromentFn(
            env=env,
            envVarName="APIAPP_VAULT_SECRET_ID",
            defaultValue=None,
            acceptableValues=None,
            nullValueAllowed=False,
            vaultClient=None
        )()

        self.client = None
        if VAULT_URL != "MOCK":
            self.client = hvac.Client(url=VAULT_URL)
            self._authenticate()

    def _authenticate(self):
        """Authenticate with Vault using the AppRole credentials."""
        if self.client is None:
            raise Exception('Vault client is not initialized - is this a mock instance?')
        auth_response = self.client.auth.approle.login(
            role_id=self.VAULT_ROLE_ID,
            secret_id=self.VAULT_SECRET_ID
        )
        if not self.client.is_authenticated():
            raise Exception("Failed to authenticate with Vault")
        print(" ✅ Authenticated with Vault")

    def _ensure_authenticated(self):
        if not self.client.is_authenticated():
            print("Token expired, re-authenticating...")
            self._authenticate()  # re-login via role_id + secret_id

    def isValidRef(self, ref):
        try:
            _, _ = ref.rsplit(":", 1)
        except ValueError:
            return False
        return True

    def registerDependantRef(self, ref):
        try:
            path, field = ref.rsplit(":", 1)
        except ValueError:
            raise ValueError("Invalid secret reference. Expected format: '<path>:<field>'")

        with self._lock:
            if path not in self.dependantRefs:
                self.dependantRefs[path] = {
                    field: {
                        "value": None,
                        "expiry": None
                    }
                }
                return
            if field not in self.dependantRefs[path]:
                self.dependantRefs[path][field] = {
                    "value": None,
                    "expiry": None
                }
                return
            # it is already registered - do nothing
            return


    def get_secret(self, ref, skipCache=False) -> str:
        if self.client is None:
            # If we don't have a client it is a mock instance so just return the full secret ref
            return ref
        try:
            path, field = ref.rsplit(":", 1)
        except ValueError:
            raise ValueError("Invalid secret reference. Expected format: '<path>:<field>'")
        self.registerDependantRef(ref)
        if not skipCache:
            with self._lock:
                if path in self.dependantRefs:
                    if field in self.dependantRefs[path]:
                        if self.dependantRefs[path][field]["value"] is not None:
                            if self.dependantRefs[path][field]["expiry"] is None:
                                # no expiry always use cache
                                return self.dependantRefs[path][field]["value"]
                            else:
                                cur_time = self.getCurDateTime()
                                if cur_time < self.dependantRefs[path][field]["expiry"]:
                                    # It haas not expired
                                    return self.dependantRefs[path][field]["value"]

        self._ensure_authenticated()
        try:
            result = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point="kv"
            )
            data = result["data"]["data"]
            if field not in data:
                raise KeyError(f"Field '{field}' not found in secret at {path}")
            expiry_time = self.getCurDateTime() + DEFAULT_EXPIRY_DURATION
            with self._lock:
                for curField in data.keys():
                    if path not in self.dependantRefs:
                        raise Exception("This should not happen - dependant ref path missing " + path)
                    if curField in self.dependantRefs[path]:
                        self.dependantRefs[path][curField] = {
                            "value": data[curField],
                            "expiry": expiry_time
                        }
                return data[field]
        except hvac.exceptions.InvalidPath:
            raise KeyError(f"Secret not found at path: {path}")
        except hvac.exceptions.Forbidden:
            raise KeyError(f"no access to secret: {path}:{field}")

    def checkAccess(self):
        for path in self.dependantRefs:
            for field in self.dependantRefs[path]:
                self.get_secret(path + ":" + field, True)
