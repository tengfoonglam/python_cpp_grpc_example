
project(arithmetic_grpc LANGUAGES CXX)

cmake_minimum_required(VERSION 3.16.0)

find_package(Protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)

add_subdirectory("${PROJECT_SOURCE_DIR}/../arithmetic" build_arithmetic)
add_subdirectory("${PROJECT_SOURCE_DIR}/../arithmetic_proto" build_arithmetic_proto)

add_subdirectory(src)
add_subdirectory(apps)
