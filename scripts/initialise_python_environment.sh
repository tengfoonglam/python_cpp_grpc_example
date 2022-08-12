#!/bin/bash

DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_DIR=${DIR}/../.venv

pushd $DIR/..

  echo "Creating virtual environment..."
  python3 -m venv ${VENV_DIR}

  echo "Activating virtual environment..."
  source ${VENV_DIR}/bin/activate

  echo "Installing development python packages"
  pip install -r requirements.txt

  echo "Installing arithmetic_proto..."
  pip install -r ./libs/arithmetic_proto/requirements.txt
  pip install -e ./libs/arithmetic_proto

  echo "Installing arithmetic_python_client..."
  pip install -r ./libs/arithmetic_python_client/requirements.txt
  pip install -e ./libs/arithmetic_python_client

popd
