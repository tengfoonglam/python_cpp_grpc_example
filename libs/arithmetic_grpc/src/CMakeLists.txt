set(HEADER_LIST
"${PROJECT_SOURCE_DIR}/include/${PROJECT_NAME}/average_service.h"
"${PROJECT_SOURCE_DIR}/include/${PROJECT_NAME}/grpc_utils.h"
"${PROJECT_SOURCE_DIR}/include/${PROJECT_NAME}/sum_client.h"
"${PROJECT_SOURCE_DIR}/include/${PROJECT_NAME}/sum_service.h"
"${PROJECT_SOURCE_DIR}/include/${PROJECT_NAME}/prime_client.h"
"${PROJECT_SOURCE_DIR}/include/${PROJECT_NAME}/prime_service.h"
"${PROJECT_SOURCE_DIR}/include/${PROJECT_NAME}/max_service.h"
"${PROJECT_SOURCE_DIR}/include/${PROJECT_NAME}/max_client.h"
)

set(SOURCE_LIST
"average_client.cc"
"average_service.cc"
"sum_client.cc"
"sum_service.cc"
"prime_client.cc"
"prime_service.cc"
"max_service.cc"
"max_client.cc"
)

add_library(
${PROJECT_NAME} STATIC
${SOURCE_LIST}
${HEADER_LIST})

set_target_properties(${PROJECT_NAME} PROPERTIES
POSITION_INDEPENDENT_CODE ON
CMAKE_CXX_STANDARD_REQUIRED ON
CMAKE_CXX_STANDARD 17
CXX_STANDARD 17
CMAKE_BUILD_TYPE "Release"
COMPILE_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")

target_include_directories(${PROJECT_NAME} PUBLIC "${PROJECT_SOURCE_DIR}/include")

target_link_libraries(${PROJECT_NAME} PUBLIC
arithmetic_proto
arithmetic
protobuf::libprotobuf
gRPC::grpc++
gRPC::grpc++_reflection)
