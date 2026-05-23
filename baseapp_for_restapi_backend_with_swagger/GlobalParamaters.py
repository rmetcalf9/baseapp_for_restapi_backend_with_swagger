import os
import json
import sys
from urllib.parse import urlparse

exceptions = dict()
def getInvalidEnvVarParamaterException(envVarName, actualValue=None, messageOverride=None):
  if envVarName not in exceptions:
    exceptions[envVarName] = InvalidEnvVarParamaterExecption(envVarName, actualValue, messageOverride)
  return exceptions[envVarName]

class InvalidEnvVarParamaterExecption(Exception):
  def __init__(self, envVarName, actualValue=None, messageOverride=None):
    message = 'Invalid value for'
    if messageOverride is not None:
      message = messageOverride
    message = message + ' ' + envVarName
    if actualValue is not None:
      message = message + ' got:' + actualValue
    super(InvalidEnvVarParamaterExecption, self).__init__(message)

missingVarFileExceptions = dict()
class MissingVarFileExceptionClass(Exception):
  def __init__(self, envVarName, fileName):
    super(MissingVarFileExceptionClass, self).__init__("Missing Environment File var=" + envVarName + " file=" + fileName)
def getMissingVarFileException(envVarName, fileName):
  if envVarName not in missingVarFileExceptions:
    missingVarFileExceptions[envVarName] = MissingVarFileExceptionClass(envVarName, fileName)
  return missingVarFileExceptions[envVarName]
class VaultValueFoundWhenUsingIncompatibleReadFunction(Exception):
  env_var_name = None
  def __init__(self, env_var_name):
    self.env_var_name = env_var_name
    super().__init__("Found VAULT environment variable for " + env_var_name + " but code uses old read method incompatible with vault")
class VaultValueFoundButMissingVaultClient(Exception):
  env_var_name = None
  def __init__(self, env_var_name):
    self.env_var_name = env_var_name
    super().__init__("Found VAULT environment variable for " + env_var_name + " but no vault client setup")
class InvalidVaultRefException(Exception):
  pass

#Read environment variable or raise an exception if it is missing and there is no default
def readFromEnviroment(env, envVarName, defaultValue, acceptableValues, nullValueAllowed=False):
  print("baseapp Future deprecation warning: readFromEnviroment used for " + envVarName + " should be migrated to getReadFromEnviromentFn")
  if envVarName + "VAULT" in env:
    raise VaultValueFoundWhenUsingIncompatibleReadFunction(envVarName)
  return getReadFromEnviromentFn(env, envVarName, defaultValue, acceptableValues, nullValueAllowed, None)()

def getReadFromEnviromentFn(env, envVarName, defaultValue, acceptableValues, nullValueAllowed, vaultClient):
  isFile = False
  isVault = False
  if envVarName.startswith("APIAPP_"):
    if envVarName + "VAULT" in env:
      if vaultClient is None:
        raise VaultValueFoundButMissingVaultClient(envVarName)
      if not vaultClient.isValidRef(env[envVarName + "VAULT"]):
        raise InvalidVaultRefException("Invalid vault ref provided in: " + envVarName)
      isVault = True
      vaultClient.registerDependantRef(env[envVarName + "VAULT"])
    elif envVarName + "FILE" in env:
      isFile = True
      print("Checking param from file for " + envVarName)
      if not os.path.isfile(env[envVarName + "FILE"]):
        raise getMissingVarFileException(envVarName, env[envVarName + "FILE"])

  def reader(skip_cache=False):
    val = None
    if envVarName not in env:
      if envVarName.startswith("APIAPP_"):
        if isFile:
          print("Reading param from file for " + envVarName)
          # recheck for existance in case file was deleted while app is running
          if not os.path.isfile(env[envVarName + "FILE"]):
            raise getMissingVarFileException(envVarName, env[envVarName + "FILE"])
          with open(env[envVarName + "FILE"], 'r') as file:
              val = file.read()
        if isVault:
          return vaultClient.get_secret(env[envVarName + "VAULT"], skip_cache)
    if val is None:
      try:
        val = env[envVarName]
      except KeyError:
        if (defaultValue is None):
          raise getInvalidEnvVarParamaterException(envVarName, None, 'Environment variable not set and no default')
        return defaultValue

    if (acceptableValues is not None):
      if (val not in acceptableValues):
        raise getInvalidEnvVarParamaterException(envVarName, val, 'Not an acceptable value')
    if not nullValueAllowed:
      if val == '':
        raise getInvalidEnvVarParamaterException(envVarName, None, 'Null/Empty String')
    return val
  return reader

# class to store GlobalParmaters
class GlobalParamatersClass():
  mode = None
  version = None
  webfrontendpath = None
  apiurl = None
  apidocsurl = None
  apiaccesssecurity = None
  APIAPP_PORT = None
  APIAPP_FRONTENDURL = None
  APIAPP_PROJECT_NAME = None

  def __init__(self, env):
    self.APIAPP_PROJECT_NAME = getReadFromEnviromentFn(env, 'APIAPP_PROJECT_NAME', None, None, False, None)()
    self.mode = getReadFromEnviromentFn(env, 'APIAPP_MODE', None, ['DEVELOPER','DOCKER'], False, None)()
    self.version = getReadFromEnviromentFn(env, 'APIAPP_VERSION', None, None, False, None)()
    self.webfrontendpath = getReadFromEnviromentFn(env, 'APIAPP_FRONTEND', None, None, False, None)()
    self.apiurl = getReadFromEnviromentFn(env, 'APIAPP_APIURL', None, None, False, None)()
    self.apidocsurl = getReadFromEnviromentFn(env, 'APIAPP_APIDOCSURL', '_', None, False, None)()
    apiaccesssecuritySTR = getReadFromEnviromentFn(env, 'APIAPP_APIACCESSSECURITY', None, None, False, None)()
    APIAPP_PORTSTR = getReadFromEnviromentFn(env, 'APIAPP_PORT', '80', None, False, None)()
    try:
      self.APIAPP_PORT = int(APIAPP_PORTSTR)
    except:
      raise getInvalidEnvVarParamaterException('APIAPP_PORT', actualValue=APIAPP_PORTSTR, messageOverride='Port must be a number')
    self.APIAPP_FRONTENDURL = getReadFromEnviromentFn(env, 'APIAPP_FRONTENDURL', 'http://UNKNOWN.com/abc/frontend', None, False, None)()

    if (self.webfrontendpath != '_'):
      if (not os.path.isdir(self.webfrontendpath)):
        raise getInvalidEnvVarParamaterException('APIAPP_FRONTEND', actualValue=self.webfrontendpath, messageOverride='Frontend directory doesn\'t exist')
    if (len(self.version) == 0):
      raise getInvalidEnvVarParamaterException('APIAPP_VERSION', actualValue=self.version, messageOverride='Version length can\'t be zero')

    #JSONDecodeError only availiable in python 3.5 and up
    errToCatch = ValueError
    if sys.version_info[0] >= 3.5:
      errToCatch = json.decoder.JSONDecodeError

    try:
      self.apiaccesssecurity = json.loads(apiaccesssecuritySTR)
    except errToCatch:
      print('Invalid JSON for apiaccesssecurity - ' + apiaccesssecuritySTR)
      raise getInvalidEnvVarParamaterException('APIAPP_APIACCESSSECURITY')

    self.ensureNotTerminatedWithASlash(self.apiurl, 'APIAPP_APIURL')
    self.ensureNotTerminatedWithASlash(self.apidocsurl, 'APIAPP_APIDOCSURL')

  def ensureNotTerminatedWithASlash(self, val, param):
    if len(val)==0:
      return
    if val[-1:] != '/':
      if val[-1:] != '\\':
        return
    raise getInvalidEnvVarParamaterException(param, actualValue=val, messageOverride='Should not end with a slash')

  def getStartupOutput(self):
    r = 'Mode:' + self.mode + '\n'
    r += 'Version:' + self.version + '\n'
    r += 'Frontend Location:' + self.webfrontendpath + '\n'
    r += 'apiurl:' + self.apiurl + '\n'
    r += 'apidocsurl:' + self.apidocsurl + '\n'
    r += 'apiaccesssecurity:' + json.dumps(self.apiaccesssecurity) + '\n'
    #Not reporting POST as flask will output that for us
    return r

  def getDeveloperMode(self):
    return (self.mode == 'DEVELOPER')

  def getWebFrontendPath(self):
    return self.webfrontendpath

  def getWebServerInfoJSON(self):
    return json.dumps({'version': self.version,'apiurl': self.apiurl,'apidocsurl': self.apidocsurl,'apiaccesssecurity': self.apiaccesssecurity})

  def getAPIHost(self):
    return urlparse(self.apiurl).netloc

  def getSanitizedPath(self, url):
    a = urlparse(url).path.strip()
    if (a[-1:] == '/'):
      a = a[:-1]
    return a

  def getAPIPath(self):
    return self.getSanitizedPath(self.apiurl)

  def overrideAPIDOCSPath(self):
    return (self.getAPIDOCSPath() != '')

  def getAPIDOCSPath(self):
    return self.getSanitizedPath(self.apidocsurl)
