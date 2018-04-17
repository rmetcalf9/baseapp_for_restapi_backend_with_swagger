# Enviroment variable configuration detail

 | Name | Example Value | Meaning |
 | ---- | ------------- | ------- |
 | APIAPP_MODE | DOCKER | Can be DEVELOPER or DOCKER. This lets applications have different behavour when run inside docker. |
 | APIAPP_VERSION | 0.0.9 | Read in from launch file to allow the code version to be stored by the application. Output in webserver info service call |
 | APIAPP_FRONTEND |  | URL the user uses to access the frontend application. This is required so internal url's in the apidocs are pointed correctly. |
 | APIAPP_APIURL |  | URL the frontend applicaton application needs to access the API. Output in webserver info service call |
 | APIAPP_APIDOCSURL |  | URL the user can use to access the Swagger UI API documentation. Output in webserver info service call |
 | APIAPP_APIACCESSSECURITY |  | Must be valid JSON. Holds information the frontend needs to access the API. E.g. basic-auth means it will prompt the user for username and password and provide that in a header whenever it calls the API. Output in webserver info service call |
 
 
