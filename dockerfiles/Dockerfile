# Base image with basic dependencies and gRPC
FROM ubuntu:20.04 AS python_cpp_grpc_base

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --no-install-recommends -y \
  autoconf=2.69-11.1 \
  automake=1:1.16.1-4ubuntu6 \
  build-essential=12.8ubuntu1.1 \
  cmake=3.16.3-1ubuntu1 \
  curl=7.68.0-1ubuntu2.12 \
  g++=4:9.3.0-1ubuntu2 \
  git=1:2.25.1-1ubuntu3.5 \
  libtool=2.4.6-14 \
  libssl-dev=1.1.1f-1ubuntu2.16 \
  make=4.2.1-1.2 \
  pkg-config=0.29.1-0ubuntu4 \
  software-properties-common=0.99.9.8 \
  wget=1.20.3-1ubuntu2 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY scripts/install_grpc.sh scripts/install_grpc.sh
RUN /bin/bash -c "source scripts/install_grpc.sh"

# Compile C++ gRPC Server
FROM python_cpp_grpc_base AS arithmetic_cpp_grpc

WORKDIR /
COPY . .

WORKDIR /libs/arithmetic_grpc/build
SHELL ["/bin/bash", "-c"]
RUN NPROC=1 && if [ "$(nproc)" -gt 1 ]; then NPROC="$(($(nproc) - 1))"; fi &&\
cmake ../ && make -j$NPROC

# Copy executable to deployment image
FROM python_cpp_grpc_base as arithmetic_server
WORKDIR /
COPY --from=arithmetic_cpp_grpc /libs/arithmetic_grpc/build/apps/arithmetic_server ./
CMD ["./arithmetic_server"]
