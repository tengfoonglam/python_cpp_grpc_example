#include <arithmetic_grpc/grpc_utils.h>
#include <arithmetic_grpc/max_client.h>
#include <grpc++/grpc++.h>

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>

using namespace arithmetic_grpc;

void RunAverageClient() {
  MaxClient client(grpc::CreateChannel(DEFAULT_GRPC_ADDRESS,
                                       grpc::InsecureChannelCredentials()));

  while (true) {
    std::vector<std::int64_t> numbers_to_max;
    bool still_entering_numbers = true;
    bool input_successful = true;

    while (still_entering_numbers) {
      std::string number_str;

      std::cout << "Enter number you want to max (leave empty to end input): ";
      std::getline(std::cin, number_str);

      if (number_str.empty()) {
        still_entering_numbers = false;
      } else {
        const std::int64_t number = std::stoi(number_str);
        std::cout << "Adding number " << number << " to be processed"
                  << std::endl;
        numbers_to_max.push_back(number);
      }
    }

    if (input_successful) {
      std::cout << "Now calculating max of ..." << std::endl;
      for (const auto number : numbers_to_max) {
        std::cout << number << " ";
      }
      std::cout << std::endl;
      auto output = client.GetMax(numbers_to_max);

      const bool computation_success = output.first;
      const float answer = output.second;

      if (computation_success) {
        std::cout << "Max: " << answer << std::endl;
      } else {
        std::cout << "Average computation failed" << std::endl;
      }

    } else {
      std::cout << "Something went wrong when entering input, restarting..."
                << std::endl;
    }
  }
}

int main() {
  RunAverageClient();
  return 0;
}
