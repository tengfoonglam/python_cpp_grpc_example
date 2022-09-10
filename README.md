# python_cpp_grpc_example

---
 ***python_cpp_grpc_example*** is an example on how to create a Python-C++ interface using [gRPC](https://grpc.io/) (gRPC Remote Procedure Calls).

The server is written in C++ while the client is in Python. Such a setup allows for performance-critical code to be written in C++ while the rest of the code is written in Python which is more productive to develop in. This is potentially very useful in robotic applications where you want your algorithms/driver code to be peformant and written in C++ but at the same time provide a user-friendly Python API for the end user.

In this project, both the C++ server Python client have been Dockerized so you can run the example without any system wide installations. However, steps to build/install the project locally are also provided.

This repository implements the 4 different service methods offered by gRPC.
 1. **gRPC Unary - Sum service**: Request takes in 2 numbers and returns a response that contains the sum
 2. **gPRC Server Streaming - Prime service**: Request takes in one integer and returns a stream of reponses that represent the prime number decomposition of that number
 3. **gRPC Client Streaming - Average service**: A stream of requests that each contains an integer and returns a response with the average of the numbers
 4. **gRPC Bi-Directional Streaming - Max service**: A stream of requests that each contains an integer and returns a stream of responses that updates the client when the maximum of the input number stream has changed

---

### Requirements
 * Docker (Installation instructions [here](https://docs.docker.com/engine/install/ubuntu/))

---

## Docker Installation

#### Building and Running C++ Arithmetic Server

 1. Build Docker images: ```./scripts/build_docker_server.sh```
 2. Deploy container: ```./scripts/launch_dockerized_cpp_grpc_arithmetic_server.sh```

#### Setting up and Running Interactive Python Clients
 1. Build Docker images: ```./scripts/build_docker_client.sh```
 2. Launch an instance of the Arithmetic Server
 3. Deploy interactive Python client container to interact with server:
      1. Average: ```./scripts/launch_dockerized_interactive_arithmetic_client.py average```
      2. Max: ```./scripts/launch_dockerized_interactive_arithmetic_client.py max```
      3. Prime: ```./scripts/launch_dockerized_interactive_arithmetic_client.py prime```
      4. Sum: ```./scripts/launch_dockerized_interactive_arithmetic_client.py sum```

---

## Local Installation

#### Building and Running C++ Arithmetic Server from Source

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

#### Setting up and Running Interactive Python Clients in Python Virtual Environment

1. Initialize Python virtual environment, pip install dependencies and arithmetic client ```source ./scripts/initialise_python_environment.sh```
2. Run Pytests (without/with verbosity):
   1. Enter arithmetic_python_client package folder ```cd libs/arithmetic_python_client/```
   2. If you have built the Docker containers: ```pytest pytest/``` / ```pytest -vvv -s --log-cli-level=INFO pytest/```
   3. If you have built from source: ```pytest  --use-local-server pytest/``` / ```pytest -vvv -s --log-cli-level=INFO --use-local-server pytest/```
3. **With the Arithmetic server running** you can launch the interactive Python clients. **In the git root directory**:
   1. Average: ```./scripts/launch_interactive_python_client.py average```
   2. Max: ```./scripts/launch_interactive_python_client.py average max```
   3. Prime: ```./scripts/launch_interactive_python_client.py average prime```
   4. Sum: ```./scripts/launch_interactive_python_client.py average sum```

---

## Evans Universal gRPC Client

gRPC Server Reflection is enabled in the arithmetic server and this enables the user to use the [Evans universal gRPC client](https://github.com/ktr0731/evans) to interact with the server using terminal commands, without the Python client. This is extremely useful in the case when you need to do quick sanity checks to ensure the server is working as expected.

1. Install [Evans](https://github.com/ktr0731/evans)
2. Launch an instance of the arithmetic server (dockerized or local executable)
3. Launch Evans```evans -r --host 0.0.0.0 --port 50051 repl```
   1. Show available services: ```show service```
   2. Show available messages: ```show message```
   3. Use a service (e.g. SumService):
      1. Select Service: ```service SumService```
      2. Call service: ```call Sum```
      3. Follow prompts from terminal to enter input
   4. Exit: ```exit```

---

## Acknowledgements

 * The arithmetic examples are adapted from this [gRPC Master Class](https://www.udemy.com/course/grpc-golang/) by [Clément Jean](https://www.udemy.com/course/grpc-golang/#instructor-1). The original course implemented these gRPC services in Go but I ported them over to C++/Python as a personal exercise.
