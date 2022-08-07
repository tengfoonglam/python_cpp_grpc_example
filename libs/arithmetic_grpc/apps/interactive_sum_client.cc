#include <arithmetic_grpc/grpc_utils.h>
#include <arithmetic_grpc/sum_client.h>
#include <grpc++/grpc++.h>

#include <cmath>
#include <iostream>
#include <string>

using namespace arithmetic_grpc;

void InteractiveSumClient() {
  SumClient sum_client(grpc::CreateChannel(DEFAULT_GRPC_ADDRESS,
                                           grpc::InsecureChannelCredentials()));

  while (true) {
    std::string number_1_str{"0"};
    std::string number_2_str{"0"};

    std::cout << "Enter first number: ";
    std::cin >> number_1_str;
    std::cout << "Enter second number: ";
    std::cin >> number_2_str;

    const float number_1 = std::stof(number_1_str);
    const float number_2 = std::stof(number_2_str);

    const float answer = sum_client.Sum(number_1, number_2);
    if (std::isnan(answer)) {
      std::cout << "gRPC failed" << std::endl;
    }

    std::cout << "gRPC returned: " << std::endl;
    std::cout << number_1 << " + " << number_2 << " = " << answer << std::endl;
  }
}

int main() {
  InteractiveSumClient();
  return 0;
}
