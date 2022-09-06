#include "arithmetic_grpc/sum_service.h"

#include <arithmetic/arithmetic.h>

#include <chrono>
#include <iostream>
#include <thread>

using arithmetic_proto::SumRequest;
using arithmetic_proto::SumService;

using grpc::ServerContext;
using grpc::Status;

namespace arithmetic_grpc {

SumServiceImpl::SumServiceImpl(const std::uint64_t simulated_processing_time_ms)
    : simulated_processing_time_ms_(simulated_processing_time_ms) {}

Status SumServiceImpl::Sum(__attribute__((unused)) ServerContext* context_ptr,
                           const SumRequest* request_ptr,
                           SumResponse* response_ptr) {
  const auto number_1 = request_ptr->number_1();
  const auto number_2 = request_ptr->number_2();
  const float answer = arithmetic::Sum(number_1, number_2);
  std::this_thread::sleep_for(std::chrono::milliseconds(
      simulated_processing_time_ms_));  // Simulate processing time
  response_ptr->set_answer(answer);
  std::cout << "Sum Service called: " << number_1 << " + " << number_2 << " = "
            << answer << std::endl;
  return Status::OK;
}

}  // namespace arithmetic_grpc
