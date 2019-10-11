# flask rest plus dependancy

This library is dependany on flask rest plus. The are various places where I have had to override parts of flask rest plus as it did not support functionality I needed .As flask rest plus updates I need to review these places to make sure my code continues to work.



# Sub class FlaskRestSubclass.py

baseapp_for_restapi_backend_with_swagger/baseapp_for_restapi_backend_with_swagger/FlaskRestSubclass.py

I use this class instead of the normal flast reat plus api. It enables me to override functions and extend them with functionality I need.



# Sub class Apidoc (blueprint)

This blueprint is provided by flask but I need to override it. Because this is now in my project I now need to import the swagger ui directory.


## Swagger ui

baseapp_for_restapi_backend_with_swagger/baseapp_for_restapi_backend_with_swagger/static/bower/swagger-ui/dist/
This entire directory is copied in task.py (assets(ctx)) near the bottom you have
 ctx.run('cp node_modules/swagger-ui-dist/{swagger-ui*.{css,js}{,.map},favicon*.png} flask_restplus/static')

these files are actually a node module
to get them:
```
mkdir t
cd t
wget https://raw.githubusercontent.com/noirbizarre/flask-restplus/master/package.json
npm install
# (gets us Swagger-UI 3.4.0)
```

Then copy the files into the correct locations:
```
GR=__REPLACE_WITH_GIT_ROOT__

cp ./node_modules/swagger-ui-dist/ ${GR}/baseapp_for_restapi_backend_with_swagger/static/bower/swagger-ui/dist/
cp ./node_modules/swagger-ui-dist/* ${GR}/baseapp_for_restapi_backend_with_swagger/static/bower/swagger-ui/dist/.
cp ./node_modules/typeface-droid-sans/index.css ${GR}/baseapp_for_restapi_backend_with_swagger/static/bower/swagger-ui/dist/droid-sans.css
cp -r ./node_modules/typeface-droid-sans/files ${GR}/baseapp_for_restapi_backend_with_swagger/static/bower/swagger-ui/dist/.
```

note: the dist directory is part of a gitignore file. You need to force add the files.

Then I copied the files from the t/node_modules/swagger-ui-dist into /static/bower/swagger-ui/dist/

????

## tempaltes directory
https://github.com/rmetcalf9/baseapp_for_restapi_backend_with_swagger/tree/master/baseapp_for_restapi_backend_with_swagger/templates
is direct copy from
https://github.com/noirbizarre/flask-restplus/tree/e73ed6532784720468b741b234fbc23961acc059/flask_restplus/templates
