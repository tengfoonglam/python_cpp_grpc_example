project(arithmetic_proto LANGUAGES C CXX)

cmake_minimum_required(VERSION 3.16.0)

# Find Packages
set(protobuf_MODULE_COMPATIBLE TRUE)
find_package(Protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)

# Generate Proto Library
set(PROTO_FILES
  "${PROJECT_NAME}/average.proto"
  "${PROJECT_NAME}/max.proto"
  "${PROJECT_NAME}/prime.proto"
  "${PROJECT_NAME}/sum.proto"
)

add_library(
${PROJECT_NAME} STATIC ${PROTO_FILES})

set_target_properties(${PROJECT_NAME} PROPERTIES
POSITION_INDEPENDENT_CODE ON
CMAKE_CXX_STANDARD_REQUIRED ON
CMAKE_CXX_STANDARD 17
CXX_STANDARD 17
CMAKE_BUILD_TYPE "Release"
COMPILE_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")

target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_CURRENT_BINARY_DIR}")

target_link_libraries(${PROJECT_NAME} PUBLIC
protobuf::libprotobuf
gRPC::grpc++
gRPC::grpc++_reflection
)

# List where to look for proto files
list(APPEND PROTO_PATHS "${PROJECT_SOURCE_DIR}")
# If you are importing protos from another library, you can append to PROTO_PATHS where to look for the .proto files. For example:
# list(APPEND PROTO_PATHS "${PROJECT_SOURCE_DIR}/../../external/external_proto_library")

# Compile protobuf and grpc files
get_target_property(grpc_cpp_plugin_location gRPC::grpc_cpp_plugin LOCATION)
protobuf_generate(TARGET ${PROJECT_NAME} LANGUAGE cpp IMPORT_DIRS ${PROTO_PATHS})
protobuf_generate(TARGET ${PROJECT_NAME} LANGUAGE grpc IMPORT_DIRS ${PROTO_PATHS} PLUGIN "protoc-gen-grpc=${grpc_cpp_plugin_location}" GENERATE_EXTENSIONS .grpc.pb.h .grpc.pb.cc)
