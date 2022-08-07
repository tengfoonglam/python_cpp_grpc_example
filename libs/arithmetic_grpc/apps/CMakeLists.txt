add_executable(average_server average_server.cc)
target_link_libraries(average_server ${PROJECT_NAME})

add_executable(interactive_average_client interactive_average_client.cc)
target_link_libraries(interactive_average_client ${PROJECT_NAME})

add_executable(sum_server sum_server.cc)
target_link_libraries(sum_server ${PROJECT_NAME})

add_executable(interactive_sum_client interactive_sum_client.cc)
target_link_libraries(interactive_sum_client ${PROJECT_NAME})

add_executable(prime_server prime_server.cc)
target_link_libraries(prime_server ${PROJECT_NAME})

add_executable(interactive_prime_client interactive_prime_client.cc)
target_link_libraries(interactive_prime_client ${PROJECT_NAME})

add_executable(max_server max_server.cc)
target_link_libraries(max_server ${PROJECT_NAME})

add_executable(arithmetic_server arithmetic_server.cc)
target_link_libraries(arithmetic_server ${PROJECT_NAME})

add_executable(interactive_max_client interactive_max_client.cc)
target_link_libraries(interactive_max_client ${PROJECT_NAME})
