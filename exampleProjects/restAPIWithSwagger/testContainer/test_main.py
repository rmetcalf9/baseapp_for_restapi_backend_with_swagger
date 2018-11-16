#Script to test a running container
import unittest
import requests

baseURL="http://virtualpresencepicture:8098"

class test_containerAPI(unittest.TestCase):
#Actual tests below

  def test_WeCanGetToSwaggerFile(self):
    result = requests.get(baseURL + "/api/swagger.json")
    self.assertEqual(result.status_code, 200)
    
