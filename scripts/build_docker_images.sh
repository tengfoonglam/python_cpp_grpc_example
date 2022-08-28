#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DOCKERFILE="./dockerfiles/Dockerfile"

pushd $DIR/..
    # Run hadolint to expose any Dockerfile issues
    docker run --rm -i hadolint/hadolint < $DOCKERFILE

    OPTION=""
    if [[ $1 = no_cache ]]; then
        echo "Building Docker Images with --no-cache option"
        OPTION="--no-cache"
    fi

    docker build $OPTION --file $DOCKERFILE --target arithmetic_cpp_grpc -t arithmetic_cpp_grpc .
    docker build $OPTION --file $DOCKERFILE --target arithmetic_server -t arithmetic_server .

popd
