import TestHelperSuperClass
import unittest
import json
import pytz
import datetime

serverInfo = {
      'Server': {
        'Version': TestHelperSuperClass.env['APIAPP_VERSION'],
        "APIAPP_APIDOCSURL": TestHelperSuperClass.env['APIAPP_APIDOCSURL']
      }
}


#@TestHelperSuperClass.wipd
class test_api(TestHelperSuperClass.testHelperAPIClient):

  def test_getServerInfo(self):
    result = self.testClient.get('/api/info/serverinfo')
    self.assertEqual(result.status_code, 200, msg="Wrong response when calling /api/info/serverinfo")
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON, serverInfo)
