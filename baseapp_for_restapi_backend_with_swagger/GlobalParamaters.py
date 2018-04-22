import os
import json
import sys
from urllib.parse import urlparse

exceptions = dict()
def getInvalidEnvVarParamaterException(envVarName):
  if envVarName not in exceptions:
    exceptions[envVarName] = InvalidEnvVarParamaterExecption(envVarName)
  return exceptions[envVarName]

class InvalidEnvVarParamaterExecption(Exception):
  def __init__(self, envVarName):
    message = 'Invalid value for ' + envVarName
    super(InvalidEnvVarParamaterExecption, self).__init__(message)

#Read environment variable or raise an exception if it is missing and there is no default
def readFromEnviroment(env, envVarName, defaultValue, acceptableValues, nullValueAllowed=False):
  try:
    val = env[envVarName]
    if (acceptableValues != None):
      if (val not in acceptableValues):
        raise getInvalidEnvVarParamaterException(envVarName)
    if not nullValueAllowed:
      if val == '':
        raise getInvalidEnvVarParamaterException(envVarName)
    return val
  except KeyError:
    if (defaultValue == None):
      raise getInvalidEnvVarParamaterException(envVarName)
    return defaultValue

# class to store GlobalParmaters
class GlobalParamatersClass():
  mode = None
  version = None
  webfrontendpath = None
  apiurl = None
  apidocsurl = None
  apiaccesssecurity = None
  
  def __init__(self, env):
    self.mode = readFromEnviroment(env, 'APIAPP_MODE', None, ['DEVELOPER','DOCKER'])
    self.version = readFromEnviroment(env, 'APIAPP_VERSION', None, None)
    self.webfrontendpath = readFromEnviroment(env, 'APIAPP_FRONTEND', None, None)
    self.apiurl = readFromEnviroment(env, 'APIAPP_APIURL', None, None)
    self.apidocsurl = readFromEnviroment(env, 'APIAPP_APIDOCSURL', '_', None)
    apiaccesssecuritySTR = readFromEnviroment(env, 'APIAPP_APIACCESSSECURITY', None, None)

    if (self.webfrontendpath != '_'):
      if (not os.path.isdir(self.webfrontendpath)):
        raise getInvalidEnvVarParamaterException('APIAPP_FRONTEND')
    if (len(self.version) == 0):
      raise getInvalidEnvVarParamaterException('APIAPP_VERSION')

    #JSONDecodeError only availiable in python 3.5 and up
    errToCatch = ValueError
    if sys.version_info[0] >= 3.5:
      errToCatch = json.decoder.JSONDecodeError

    try:
      self.apiaccesssecurity = json.loads(apiaccesssecuritySTR)
    except errToCatch:
      print('Invalid JSON for apiaccesssecurity - ' + apiaccesssecuritySTR)
      raise getInvalidEnvVarParamaterException('APIAPP_APIACCESSSECURITY')

  def getStartupOutput(self):
    r = 'Mode:' + self.mode + '\n'
    r += 'Version:' + self.version + '\n'
    r += 'Frontend Location:' + self.webfrontendpath + '\n'
    r += 'apiurl:' + self.apiurl + '\n'
    r += 'apidocsurl:' + self.apidocsurl + '\n'
    r += 'apiaccesssecurity:' + json.dumps(self.apiaccesssecurity) + '\n'
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


