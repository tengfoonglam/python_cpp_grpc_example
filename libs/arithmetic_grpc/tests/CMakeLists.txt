include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)

FetchContent_MakeAvailable(googletest)

set(TEST_SRCS
  sum_server_client_test.cc
)

add_executable(test_arithmetic_grpc ${TEST_SRCS})
target_link_libraries(
  test_arithmetic_grpc PRIVATE
  gtest_main
  arithmetic_grpc
)

set_target_properties(test_arithmetic_grpc PROPERTIES
  CMAKE_CXX_STANDARD test_arithmetic_grpc
  CXX_STANDARD 17
  CMAKE_BUILD_TYPE "Release"
  COMPILE_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra"
)

add_test(
  NAME test_arithmetic_grpc
  COMMAND $<TARGET_FILE:test_arithmetic_grpc>
)
