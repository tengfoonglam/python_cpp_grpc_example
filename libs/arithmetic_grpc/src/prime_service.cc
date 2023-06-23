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

inline auto getTimeNs() {
  const auto now = std::chrono::system_clock::now();
  return std::chrono::time_point_cast<std::chrono::nanoseconds>(now)
      .time_since_epoch()
      .count();
}

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

  std::cout << "Starting sending continuous messages at "
            << simulated_processing_time_ms_ << " ms intervals";

  while (true) {
    std::this_thread::sleep_for(std::chrono::milliseconds(
        simulated_processing_time_ms_));  // Simulate processing time

    const auto timestampNs = getTimeNs();
    std::cout << "Sending timestamp " << timestampNs << std::endl;

    PerformPrimeNumberDecompositionResponse response;
    response.set_factor(timestampNs);
    const bool write_success = response_writer_ptr->Write(response);

    if (!write_success || context_ptr->IsCancelled()) {
      success = false;
      std::cout << "Failed to write all primes to client, most likely client "
                   "cancelled/terminated"
                << std::endl;
      break;
    }
  }

  std::cout << "Completed service" << std::endl;

  return success ? Status::OK : Status::CANCELLED;
}

}  // namespace arithmetic_grpc
