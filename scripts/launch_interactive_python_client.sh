#!/bin/bash

DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
APPS_DIR=${DIR}/../libs/arithmetic_python_client/apps

SERVICE="sum"
if [[ $1 = average ]]
then
  SERVICE="average"
elif [[ $1 = max ]]
then
  SERVICE="max"
elif [[ $1 = prime ]]
then
  SERVICE="prime"
elif [[ $1 = sum ]]
then
  SERVICE="sum"
else
  echo "No/invalid service name provided, starting ${SERVICE} client by default"
fi

echo "Launching interactive ${SERVICE} python client"
$APPS_DIR/interactive_${SERVICE}_client.py
