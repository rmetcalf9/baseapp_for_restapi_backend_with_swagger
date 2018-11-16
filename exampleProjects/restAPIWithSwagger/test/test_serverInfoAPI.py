from TestHelperSuperClass import testHelperAPIClient, env
import unittest
import json

class test_api(testHelperAPIClient):

  def test_getServerInfo(self):
    expRes = {
      'Server': {
        'Version': env['APIAPP_VERSION']
      },
    }
    result = self.testClient.get('/api/serverinfo/')
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    self.assertJSONStringsEqual(resultJSON, expRes)

  def test_swaggerJSONProperlyShared(self):
    result = self.testClient.get('/api/swagger.json')
    self.assertEqual(result.status_code, 200)
    result = self.testClient.get('/apidocs/swagger.json')
    self.assertEqual(result.status_code, 200)
