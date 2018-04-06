import unittest
import baseapp_for_restapi_backend_with_swagger

class test_APIBackendWithSwaggerAppObj(unittest.TestCase):
  def test_simple(self):
    a = baseapp_for_restapi_backend_with_swagger.AppObj()
    a.ttt()
