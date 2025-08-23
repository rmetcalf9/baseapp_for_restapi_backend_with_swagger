#!/bin/bash

echo 'To test one file pass filename as first param'
echo 'e.g. sudo ./continous_test.sh wip'

export PYTHONWARNINGS="ignore::DeprecationWarning"

if [ $# -eq 0 ]; then
  until ack -f --python  ./baseapp_for_restapi_backend_with_swagger ./tests | entr -d python3 -m pytest -x ./tests; do sleep 1; done
else
  echo "Only testing tagged - ${1}"
  until ack -f --python  ./baseapp_for_restapi_backend_with_swagger ./tests | entr -d python3 -m pytest -x -a ${1} ./tests; do sleep 1; done
fi
