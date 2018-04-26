import unittest
from baseapp_for_restapi_backend_with_swagger import FlaskRestSubclass
from urllib.parse import urlparse


#  def setExtraParams(apidocsurl, APIDOCSPath, overrideAPIDOCSPath, APIPath):


def getSanitizedPath(url):
  a = urlparse(url).path.strip()
  if (a[-1:] == '/'):
    a = a[:-1]
  return a

apidocsurl = "https://cat-sdts.metcarob-home.com/dockjobapidocs/"
APIDOCSPath = getSanitizedPath(apidocsurl)
overrideAPIDOCSPath = None
APIPath = None



class test_FlaskRestSubclass(unittest.TestCase):
 
    def test(self):
      pass



