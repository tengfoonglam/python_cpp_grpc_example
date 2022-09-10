#!/bin/bash

SERVICE="sum"
if [ $# -eq 0 ]
  then
  echo "No arguments supplied, will start ${SERVICE} client"
else
  SERVICE=$1
fi

docker run --init -it --env SERVICE=$SERVICE --network="host" interactive_arithmetic_client
