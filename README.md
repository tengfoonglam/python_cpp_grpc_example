# python_cpp_grpc_example

---
 ***python_cpp_grpc_example*** is an example on how to create a Python-C++ interface using [gRPC](https://grpc.io/).

The server is written in C++ while the client is in Python. Such a setup allows for performance-critical code to be written in C++ while the rest of the code is written in Python which is more productive to develop in. In this example, the C++ server is Dockerized while the Python client can be run in a Python virtual environment so you can run the example without any system wide installations (unless you want to).

This repository implements the 4 different service methods offered by gRPC.
 1. gRPC Unary - Sum service: Request takes in 2 numbers and returns a response that contains the sum
 2. gPRC Server Streaming - Prime service: Request takes in one integer and returns a stream of reponses that represent the prime number decomposition of that number
 3. gRPC Client Streaming - Average service: A stream of requests that each contains an integer and returns a response with the average of the numbers
 4. gRPC Bi-Directional Streaming - Max service: A stream of requests that each contains an integer and returns a stream of responses that updates the client when the maximum of the input number stream has changed

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

## Setting up and Running Python Clients in Python Virtual Environment

1. Initialize Python virtual environment and pip install dependencies and client ```./scripts/initialise_python_environment.sh```
2. Enter arithmetic_python_client package folder ```cd libs/arithmetic_python_client/```
3. Run Pytests (You must have built the Docker images) ```pytest```
4. With the Arithmetic server running you can launch the interactive clients:
   1. 1
   2. 2
   3. 3
   4. 4
