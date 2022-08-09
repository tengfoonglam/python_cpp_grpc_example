# python_cpp_grpc_example

---
 ***python_cpp_grpc_example*** is an example on how to create a Python-C++ interface using [gRPC](https://grpc.io/).

 ### Building and Running C++ Arithmetic Server using Docker

 1. Install Docker (instructions [here](https://docs.docker.com/engine/install/ubuntu/))
 2. Build Docker images: ```./scripts/build_docker_images.sh```
 3. Deploy container: ```./scripts/launch_dockerized_cpp_grpc_arithmetic_server.sh```

### Building and Running C++ Arithmetic Server from Source

1. Install gRPC: ```source scripts/install_grpc.sh```
2. Build arithmetic_grpc package
   - ```cd libs/arithmetic_grpc/```
   - ```mkdir build && cd build```
   - ```cmake ../ && make -j$(($(nproc) - 1))```
   - Run ctests: ```ctest```
   - Launch arithmetic server: ```./apps/arithmetic_server```
   - Other Apps you can launch:
     - Individual services / interactive clients:
        1. ```./apps/average_server``` / ```./apps/interactive_average_client```
        2. ```./apps/max_server``` / ```./apps/interactive_max_client```
        3. ```./apps/prime_server``` / ```./apps/interactive_prime_client```
        4. ```./apps/sum_server``` / ```./apps/interactive_sum_client```
