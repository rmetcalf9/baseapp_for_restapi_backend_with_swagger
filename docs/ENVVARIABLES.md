# Enviroment variable configuration detail

 | Name | Example Value | Meaning |
 | ---- | ------------- | ------- |
 | APIAPP_MODE | DOCKER | Can be DEVELOPER or DOCKER. If it is set to DEVELOPER then the application will emmit Access-Control-Allow-* headers to allow for testing API's when called from browsers. This should never be set in production enviroments. |
 | APIAPP_VERSION | 0.0.9 | Read in from launch file to allow the code version to be stored by the application. Output in webserver info service call |
 | APIAPP_FRONTEND |  | URL the user uses to access the frontend application. This is required so internal url's in the apidocs are pointed correctly. This should not be terminated with a slash. |
 | APIAPP_APIURL |  | URL the frontend applicaton application needs to access the API. Output in webserver info service call. This should not be terminated with a slash. |
 | APIAPP_APIDOCSURL |  | URL the user can use to access the Swagger UI API documentation. Output in webserver info service call. This should not be terminated with a slash. |
 | APIAPP_APIACCESSSECURITY |  | Must be valid JSON. Holds information the frontend needs to access the API. E.g. basic-auth means it will prompt the user for username and password and provide that in a header whenever it calls the API. Output in webserver info service call |
 | APIAPP_FRONTENDURL |  | URL the users access to view the frontend. This isn't used apart from for setting redirect url when the frontend is called without a slash. This is an optional paramater but if it isn't set redirects are sent to http://UNKNOWN.com/abc/frontend which is broken. This should not be terminated with a slash. |
 
