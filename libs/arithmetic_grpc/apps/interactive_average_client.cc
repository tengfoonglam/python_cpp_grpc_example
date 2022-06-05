#include <arithmetic_grpc/average_client.h>
#include <arithmetic_grpc/grpc_utils.h>
#include <grpc++/grpc++.h>

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>

using namespace arithmetic_grpc;

void RunAverageClient() {
  AverageClient client(grpc::CreateChannel(DEFAULT_GRPC_ADDRESS,
                                           grpc::InsecureChannelCredentials()));

  while (true) {
    bool still_entering_numbers = true;
    bool input_successful = true;

    while (still_entering_numbers) {
      std::string number_str;

      std::cout
          << "Enter number you want to average (leave empty to end input): ";
      std::getline(std::cin, number_str);

      if (number_str.empty()) {
        still_entering_numbers = false;
      } else {
        const std::int32_t number = std::stoi(number_str);
        std::cout << "Adding number " << number << " into average..."
                  << std::endl;
        if (!client.AddNumber(number)) {
          input_successful = false;
          still_entering_numbers = false;
        }
      }
    }

    if (input_successful) {
      std::cout << "Now calculating..." << std::endl;
      auto output = client.ComputeAverage();

      const bool computation_success = output.first;
      const float answer = output.second;

      if (computation_success) {
        std::cout << "Average: " << answer << std::endl;
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
