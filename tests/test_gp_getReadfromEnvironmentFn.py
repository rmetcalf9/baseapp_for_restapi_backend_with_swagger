from TestHelperSuperClass import testHelperSuperClass
from baseapp_for_restapi_backend_with_swagger import getReadFromEnviromentFn, getMissingVarFileException, VaultValueFoundButMissingVaultClient, VaultClient, InvalidVaultRefException
import datetime
import pytz

def getCurDateTime():
    return datetime.datetime.now(pytz.timezone("UTC"))


class test_gp_ReadFromEnvironment(testHelperSuperClass):
  appDir='.' #os.path.join('..','app')

  def test_readFromFile(self):
      env = {
          'APIAPP_MODE': 'DOCKER',
          'APIAPP_VERSION': 'TEST-3.3.3',
          'APIAPP_FRONTEND': self.appDir,
          'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
          'APIAPP_APIACCESSSECURITY': '[]',
          'APIAPP_PORT': '3456',
          'APIAPP_SOMESTRINGFROMFILEXXFILE': './tests/envSingle'
      }
      self.assertEqual(getReadFromEnviromentFn(env, "APIAPP_SOMESTRINGFROMFILEXX", None, None, False, None)(),
                       "Example Single Line Env File\n", msg="Wrong value read from file")

  def test_readFromFileNotExisting(self):
      env = {
          'APIAPP_MODE': 'DOCKER',
          'APIAPP_VERSION': 'TEST-3.3.3',
          'APIAPP_FRONTEND': self.appDir,
          'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
          'APIAPP_APIACCESSSECURITY': '[]',
          'APIAPP_PORT': '3456',
          'APIAPP_SOMESTRINGFROMFILEXXFILE': '/a/b/c'
      }
      with self.assertRaises(Exception) as context:
          self.assertEqual(getReadFromEnviromentFn(env, "APIAPP_SOMESTRINGFROMFILEXX", None, None, False, None)())
      self.checkGotRightException(context, getMissingVarFileException('APIAPP_SOMESTRINGFROMFILEXX', 'aa'))

  def test_readFromFileJSON(self):
      env = {
          'APIAPP_MODE': 'DOCKER',
          'APIAPP_VERSION': 'TEST-3.3.3',
          'APIAPP_FRONTEND': self.appDir,
          'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
          'APIAPP_APIACCESSSECURITY': '[]',
          'APIAPP_PORT': '3456',
          'APIAPP_SOMESTRINGFROMFILEXXFILE': './tests/envSomeJSON'
      }
      self.assertEqual(getReadFromEnviromentFn(env, "APIAPP_SOMESTRINGFROMFILEXX", None, None, False, None)(),
                       '{"Type": "SQLAlchemy","connectionString":"mysql+pymysql://dsafdsa:aaa@saddsa.eu-west-2.rds.amazonaws.com/dsffds","ssl_ca": "/rds-combined-ca-bundle.pem"}',
                       msg="Wrong value read from file")

  def test_readFromFileMultiLine(self):
      env = {
          'APIAPP_MODE': 'DOCKER',
          'APIAPP_VERSION': 'TEST-3.3.3',
          'APIAPP_FRONTEND': self.appDir,
          'APIAPP_APIURL': 'http://apiurlxxx:45/aa/bb/cc',
          'APIAPP_APIACCESSSECURITY': '[]',
          'APIAPP_PORT': '3456',
          'APIAPP_SOMESTRINGFROMFILEXXFILE': './tests/envMultiLine'
      }
      self.assertEqual(getReadFromEnviromentFn(env, "APIAPP_SOMESTRINGFROMFILEXX", None, None, False, None)(),
                       "Example Multi Line Env File\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\n",
                       msg="Wrong value read from file")

  def test_vaultVarWrongModeError(self):
      env = {
          'APIAPP_MODE': 'DEVELOPER',
          'APIAPP_VERSION': 'TEST-1.2.3',
          'APIAPP_FRONTEND': '_',
          'APIAPP_APIURL': 'http://apiurl',
          'APIAPP_APIACCESSSECURITY': '[]',
          'APIAPP_TESTVAULT': 'dummy'
      }
      with self.assertRaises(VaultValueFoundButMissingVaultClient) as context:
          _ = getReadFromEnviromentFn(env, "APIAPP_TEST", None, None, False, None)()

  def test_invalidVaultRef(self):
      env = {
          'APIAPP_MODE': 'DEVELOPER',
          'APIAPP_VERSION': 'TEST-1.2.3',
          'APIAPP_FRONTEND': '_',
          'APIAPP_APIURL': 'http://apiurl',
          'APIAPP_APIACCESSSECURITY': '[]',
          'APIAPP_TESTVAULT': 'dummyInvalidVaultRef',
          'APIAPP_VAULT_URL': 'MOCK',
          'APIAPP_VAULT_ROLE_ID': None,
          'APIAPP_VAULT_SECRET_ID': None
      }
      vaultClient = VaultClient(env, getReadFromEnviromentFn, getCurDateTime)
      with self.assertRaises(InvalidVaultRefException) as context:
          _ = getReadFromEnviromentFn(env, "APIAPP_TEST", None, None, False, vaultClient)()

  def test_vaultLookup(self):
      env = {
          'APIAPP_MODE': 'DEVELOPER',
          'APIAPP_VERSION': 'TEST-1.2.3',
          'APIAPP_FRONTEND': '_',
          'APIAPP_APIURL': 'http://apiurl',
          'APIAPP_APIACCESSSECURITY': '[]',
          'APIAPP_TESTVAULT': 'dummyInvalidVaultRef:abc',
          'APIAPP_VAULT_URL': 'MOCK',
          'APIAPP_VAULT_ROLE_ID': None,
          'APIAPP_VAULT_SECRET_ID': None
      }
      vaultClient = VaultClient(env, getReadFromEnviromentFn, getCurDateTime)
      self.assertEqual(
          getReadFromEnviromentFn(env, "APIAPP_TEST", None, None, False, vaultClient)(),
          "dummyInvalidVaultRef:abc"
      )

