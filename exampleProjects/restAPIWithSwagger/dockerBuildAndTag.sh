#!/bin/bash

echo "Executing docker build"
export START_DIR=$(pwd)
cd ${START_DIR}

export GITROOT=$(pwd)
export CMD_DOCKER=docker
export CMD_GIT=git



DOCKER_USERNAME=TODOENTER
DOCKER_IMAGENAME=TODOENTER
cd ${GITROOT}

echo "Ensuring there are no local changes"
if [[ `${CMD_GIT} status --porcelain` ]]; then
  echo ""
  echo "Error - there are local changes commit these before continuing"
  exit 1
fi

VERSIONFILE=${GITROOT}/VERSION
cd ${START_DIR}
./bumpVersion.sh ${VERSIONFILE}
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Bump version failed"
  exit 1
fi
VERSIONNUM=$(cat ${VERSIONFILE})

# must build AFTER the version is bumped as the version file is imported to the image
cd ${GITROOT}
eval ${CMD_DOCKER} build . -t ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:latest
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Docker build failed"
  exit 1
fi

cd ${GITROOT}
${CMD_GIT} add -A
${CMD_GIT} commit -m "version ${VERSIONNUM}"
${CMD_GIT} tag -a "${VERSIONNUM}" -m "version ${VERSIONNUM}"
${CMD_GIT} push
RES=$?
if [ ${RES} -ne 0 ]; then
  cd ${START_DIR}
  echo ""
  echo "Failed to push to git. You need to run the following commands manually to complete:"f
  echo " git push"
  echo " git push --tags"
  echo " ${CMD_DOCKER} tag ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:latest ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}"
  exit 1
fi

${CMD_GIT} push --tags
${CMD_DOCKER} tag ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:latest ${DOCKER_USERNAME}/${DOCKER_IMAGENAME}:${VERSIONNUM}


echo "Script Complete"

cd ${START_DIR}
exit 0
