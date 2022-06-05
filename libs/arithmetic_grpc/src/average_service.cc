#include "arithmetic_grpc/average_service.h"

#include <arithmetic/arithmetic.h>

namespace arithmetic_grpc {

Status AverageServiceImpl::Average(__attribute__((unused))
                                   ServerContext* context_ptr,
                                   ServerReader<AverageRequest>* reader_ptr,
                                   AverageResponse* response_ptr) {
  AverageRequest request;
  std::vector<std::int32_t> numbers_to_average;

  while (reader_ptr->Read(&request)) {
    std::cout << "Received input " << request.number() << std::endl;
    numbers_to_average.push_back(request.number());
  }
  std::cout << "Received all input, now computing average ..." << std::endl;
  const float answer = arithmetic::ComputeAverage(numbers_to_average);
  response_ptr->set_answer(answer);
  std::cout << "Answer: " << answer << std::endl;

  return Status::OK;
}

}  // namespace arithmetic_grpc
