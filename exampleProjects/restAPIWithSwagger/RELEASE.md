# Release process for new container version

Run all the following from the /server directory.

Code change
continous test works

Build and tag a new docker image
```
dockerBuildAndTag.sh
```

Run the newly created container
```
docker run --network pythontestingnetwork --name virtualpresencepicture -p 8098:8098 -e APIAPP_APIURL="${EXTURL}:${EXTPORT}/api" -e APIAPP_APIDOCSURL="${EXTURL}:${EXTPORT}/apidocs" -d metcarob/virtualpresencepicture:latest
```

Run tests against the container and make sure it is working
```
docker run --network pythontestingnetwork --mount type=bind,source=$(pwd),target=/ext_volume metcarob/virtualpresencepicturetest:latest nosetests --rednose /ext_volume/testContainer
```

Clean up and push change to git
```
docker stop virtualpresencepicture
docker rm virtualpresencepicture
```

The new version and tag is already created. If the container fails the tests don't go into the docker hub and trigger the build.

Update docker hub version of the image
```
log into docker hub
Press trigger build
```

# Prerequrisites:

Build the release container image (goto ./testContainer/ and run docker build . -t metcarob/virtualpresencepicturetest:latest)
Create network
sudo docker network create pythontestingnetwork
