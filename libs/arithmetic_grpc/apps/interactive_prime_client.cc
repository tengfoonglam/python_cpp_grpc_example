#include <arithmetic_grpc/grpc_utils.h>
#include <arithmetic_grpc/prime_client.h>
#include <grpc++/grpc++.h>

#include <cstdint>
#include <iostream>
#include <string>

using namespace arithmetic_grpc;

void InteractivePrimeClient() {
  PerformPrimeNumberDecompositionClient prime_client(grpc::CreateChannel(
      DEFAULT_GRPC_ADDRESS, grpc::InsecureChannelCredentials()));

  while (true) {
    std::string number_str;

    std::cout << "Enter number to perform prime number decomposition for: ";
    std::cin >> number_str;

    const std::uint64_t number = std::stoll(number_str);

    const auto answer = prime_client.PerformPrimeNumberDecomposition(number);

    std::cout << "gRPC returned: " << std::endl;

    bool first_element_printed = false;
    std::cout << "(";
    for (const auto prime_number : answer) {
      if (first_element_printed) {
        std::cout << " , ";
      }
      std::cout << prime_number;
      first_element_printed = true;
    }
    std::cout << ")" << std::endl;
  }
}

int main() {
  InteractivePrimeClient();
  return 0;
}
