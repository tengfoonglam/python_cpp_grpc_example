#include "arithmetic_grpc/prime_service.h"

#include <arithmetic/arithmetic.h>

#include <chrono>
#include <cstdint>
#include <iostream>
#include <thread>

using arithmetic_proto::PerformPrimeNumberDecompositionRequest;
using arithmetic_proto::PerformPrimeNumberDecompositionService;

using grpc::ServerContext;
using grpc::Status;

namespace arithmetic_grpc {

PerformPrimeNumberDecompositionServiceImpl::
    PerformPrimeNumberDecompositionServiceImpl(
        std::uint64_t simulated_processing_time_ms)
    : simulated_processing_time_ms_(simulated_processing_time_ms) {}

Status
PerformPrimeNumberDecompositionServiceImpl::PerformPrimeNumberDecomposition(
    __attribute__((unused)) ServerContext* context_ptr,
    const PerformPrimeNumberDecompositionRequest* request_ptr,
    ServerWriter<PerformPrimeNumberDecompositionResponse>*
        response_writer_ptr) {
  bool success = true;
  const auto number_to_process = request_ptr->number();
  const auto prime_numbers =
      arithmetic::GetPrimeNumberDecomposition(number_to_process);

  std::cout
      << "Perform Prime Number Decomposition Service requested for number: "
      << number_to_process << std::endl;

  for (const auto prime_number : prime_numbers) {
    std::this_thread::sleep_for(std::chrono::milliseconds(
        simulated_processing_time_ms_));  // Simulate processing time

    std::cout << "Sending prime " << prime_number << std::endl;

    PerformPrimeNumberDecompositionResponse response;
    response.set_factor(prime_number);
    const bool write_success = response_writer_ptr->Write(response);

    if (!write_success || context_ptr->IsCancelled()) {
      success = false;
      std::cout << "Failed to write all primes to client, most likely client "
                   "cancelled/terminated"
                << std::endl;
      break;
    }
  }

  std::cout << "Completed Prime Number Decomposition Service for number: "
            << number_to_process << std::endl;

  return success ? Status::OK : Status::CANCELLED;
}

}  // namespace arithmetic_grpc
