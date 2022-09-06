#include "arithmetic_grpc/average_service.h"

#include <arithmetic/arithmetic.h>

#include <iostream>

namespace arithmetic_grpc {

Status AverageServiceImpl::Average(__attribute__((unused))
                                   ServerContext* context_ptr,
                                   ServerReader<AverageRequest>* reader_ptr,
                                   AverageResponse* response_ptr) {
  AverageRequest request;
  std::vector<std::int32_t> numbers_to_average;

  std::cout << "Average Service started" << std::endl;

  while (reader_ptr->Read(&request)) {
    std::cout << "Received input " << request.number() << std::endl;
    numbers_to_average.push_back(request.number());
  }

  const auto service_cancelled = context_ptr->IsCancelled();

  if (service_cancelled) {
    std::cout << "Average Service has been cancelled midway, will not compute "
                 "average"
              << std::endl;
  } else {
    std::cout << "Received all input, now computing average ..." << std::endl;
    const float answer = arithmetic::ComputeAverage(numbers_to_average);
    response_ptr->set_answer(answer);
    std::cout << "Answer: " << answer << std::endl;
  }

  std::cout << "Average Service completed" << std::endl;

  return !service_cancelled ? Status::OK : Status::CANCELLED;
}

}  // namespace arithmetic_grpc
