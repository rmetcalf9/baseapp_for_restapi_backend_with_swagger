from baseapp_for_restapi_backend_with_swagger import FlaskRestSubclass
from TestHelperSuperClass import testHelperAPIClient

class test_AppObjAPI(testHelperAPIClient):

  def test_checkSwaggerJsonFiles(self):
    #Tests all locations for swagger files
    result = self.testClient.get('/api/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/apis/swagger.json for api not present')
    result = self.testClient.get('/apidocs/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/apidocs/swagger.json for apidocs not present')
    result = self.testClient.get('/ebos/GenderV1/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/ebos/GenderV1/swagger.json for Gender api not present')
    result = self.testClient.get('/ebodocs/GenderV1/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/ebodocs/GenderV1/swagger.json for Gender apidocs not present')
    result = self.testClient.get('/ebos/AnimalsV1/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/ebos/AnimalsV1/swagger.json for Animals api not present')
    result = self.testClient.get('/ebodocs/AnimalsV1/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/ebodocs/AnimalsV1/swagger.json for Animals apidocs not present')

  def test_docsIndexesPresent(self):
    #Tests all locations for swagger files
    result = self.testClient.get('/apidocs/')
    self.assertEqual(result.status_code, 200, msg='/apidocs/ not present')
    result = self.testClient.get('/ebodocs/GenderV1/')
    self.assertEqual(result.status_code, 200, msg='/ebodocs/GenderV1/ not present')
    result = self.testClient.get('/ebodocs/AnimalsV1/')
    self.assertEqual(result.status_code, 200, msg='/ebodocs/AnimalsV1/ not present')
