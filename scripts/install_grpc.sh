#!/bin/bash

# Only run sudo if executed locally
SUDO=''
if ! [ -f /.dockerenv ]; then
    SUDO='sudo'
fi

# Run with nproc-1 unless there is only one processor
NPROC=1
if [ "$(nproc)" > 1 ]; then
    NPROC="$(($(nproc) - 1))"
fi
echo "Building with $NPROC processor(s)"

# Set environmental variables to install gRPC (if not in docker container, install locally in .local folder)
if ! [ -f /.dockerenv ]; then
    MY_INSTALL_DIR=$HOME/.local
else
    MY_INSTALL_DIR=/usr/local
fi

mkdir -p $MY_INSTALL_DIR
export PATH="$MY_INSTALL_DIR/bin:$PATH"

# Clone Repository
git clone --recurse-submodules -b v1.45.0 https://github.com/grpc/grpc

# Build and install grpc
cd grpc
mkdir -p cmake/build
pushd cmake/build
    cmake -DgRPC_INSTALL=ON \
        -DgRPC_BUILD_TESTS=OFF \
        -DCMAKE_INSTALL_PREFIX=$MY_INSTALL_DIR \
        ../..
    make -j$NPROC
    make install
popd

# Remove repository after installation
cd ..
$SUDO rm -r grpc
