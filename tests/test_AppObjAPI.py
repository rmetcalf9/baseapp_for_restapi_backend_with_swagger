from baseapp_for_restapi_backend_with_swagger import FlaskRestSubclass
from TestHelperSuperClass import testHelperAPIClient

class test_AppObjAPI(testHelperAPIClient):

  def test_checkSwaggerJsonFiles(self):
    #Tests all locations for swagger files
    result = self.testClient.get('/api/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/apis/swagger.json for api not present')
    result = self.testClient.get('/apidocs/swagger.json')
    self.assertEqual(result.status_code, 200, msg='/apidocs/swagger.json for apidocs not present')


  def test_docsIndexesPresent(self):
    #print("*********DEBUG RULE START*************")
    #for rule in self.appObj.flaskAppObject.url_map.iter_rules():
    #  print(rule)
    #print("*********DEBUG RULE END*************")
    
    #Tests all locations for swagger files
    #  this verifys the templates
    result = self.testClient.get('/apidocs/')
    self.assertEqual(result.status_code, 200, msg='/apidocs/ not present')

  def test_checkStatics(self):
    result = self.testClient.get('/apidocs/swaggerui/bower/swagger-ui/dist/css/typography.css')
    self.assertEqual(result.status_code, 200, msg='Could not find sample static')
    

  def test_apidocs_redirect_bad_URLs(self):
    result = self.testClient.get('/apidocs')
    self.assertEqual(result.status_code, 301)
    self.assertEqual(result.headers['location'], 'http://apiurlxxx/apidocs/')

    #/api/ is never registered so will never redirect badly
    #result = self.testClient.get('/api')
    #self.assertEqual(result.status_code, 301)
    #self.assertEqual(result.headers['location'], 'http://localhost:3033/api/')

    result = self.testClient.get('/frontend')
    self.assertEqual(result.status_code, 301)
    self.assertEqual(result.headers['location'], 'http://UNKNOWN.com/abc/frontend/')
