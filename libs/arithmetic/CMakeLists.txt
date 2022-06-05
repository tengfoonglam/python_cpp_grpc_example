project(arithmetic LANGUAGES C CXX)

cmake_minimum_required(VERSION 3.16.0)

add_library(${PROJECT_NAME} INTERFACE)
target_include_directories(${PROJECT_NAME} INTERFACE "${PROJECT_SOURCE_DIR}/include")

enable_testing() # Enable ctest for the project
add_subdirectory(tests)