# Base image with basic dependencies and gRPC
FROM ubuntu:20.04 AS python_cpp_grpc_base

ARG DEBIAN_FRONTEND=noninteractive

# hadolint ignore=DL3008
RUN apt-get update && apt-get install --no-install-recommends -y \
  autoconf \
  automake \
  build-essential \
  cmake \
  curl \
  g++ \
  git \
  libtool \
  libssl-dev \
  make \
  pkg-config \
  software-properties-common \
  wget \
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
