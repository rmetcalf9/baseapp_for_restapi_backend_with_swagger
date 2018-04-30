#Test helper functions
# defines a baseclass with extra functions
# https://docs.python.org/3/library/unittest.html
import unittest
import json
from baseapp_for_restapi_backend_with_swagger import AppObjBaseClass, from_iso8601

import datetime
import pytz


env = {
  'APIAPP_MODE': 'DOCKER',
  'APIAPP_VERSION': 'TEST-3.3.3',
  'APIAPP_FRONTEND': '.',
  'APIAPP_APIURL': 'http://apiurlxxx',
  'APIAPP_APIDOCSURL': 'http://apiurlxxx/apidocs',
  'APIAPP_APIACCESSSECURITY': '[{ "type": "basic-auth" }]',
  'APIAPP_USERFORJOBS': 'root',
  'APIAPP_GROUPFORJOBS': 'root',
  'APIAPP_SKIPUSERCHECK': True,
}
appObjGlobInst = AppObjBaseClass()
appObjGlobInst.init(env, testingMode = True)

class testHelperSuperClass(unittest.TestCase):
  def checkGotRightException(self, context, ExpectedException):
    if (context.exception != None):
      if (context.exception != ExpectedException):
        print("**** Wrong exception raised:")
        print("      expected: " + type(ExpectedException).__name__ + ' - ' + str(ExpectedException));
        print("           got: " + type(context.exception).__name__ + ' - ' + str(context.exception));
        raise context.exception
    self.assertTrue(ExpectedException == context.exception)

  def areJSONStringsEqual(self, str1, str2):
    a = json.dumps(str1, sort_keys=True)
    b = json.dumps(str2, sort_keys=True)
    return (a == b)

  def assertJSONStringsEqual(self, str1, str2, msg=''):
    if (self.areJSONStringsEqual(str1,str2)):
      return
    print("Mismatch JSON")
    a = json.dumps(str1, sort_keys=True)
    b = json.dumps(str2, sort_keys=True)
    print(a)
    print("--")
    print(b)
    self.assertTrue(False, msg=msg)

  def assertTimeCloseToCurrent(self, time, msg='Creation time is more than 3 seconds adrift'):
    if (isinstance(time, str)):
      time = from_iso8601(time)
    curTime = datetime.datetime.now(pytz.timezone("UTC"))
    time_diff = (curTime - time).total_seconds()
    self.assertTrue(time_diff < 3, msg=msg)
    
#helper class with setup for an APIClient
class testHelperAPIClient(testHelperSuperClass):
  testClient = None
  appObj = None

  def setUp(self):
    global appObjGlobInst
    # curDatetime = datetime.datetime.now(pytz.utc)
    # for testing always pretend the server started at a set datetime
    self.appObj = appObjGlobInst
    self.testClient = self.appObj.flaskAppObject.test_client()
    self.testClient.testing = True 
  def tearDown(self):
    self.testClient = None

  def findRecord(self, params, name):
    for cur in params:
      if (name==params[cur]['name']):
        return params[cur]
    return None



