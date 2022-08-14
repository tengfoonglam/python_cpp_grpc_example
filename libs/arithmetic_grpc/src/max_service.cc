#include "arithmetic_grpc/max_service.h"

#include <arithmetic/arithmetic.h>

#include <cstdint>
#include <iostream>

namespace arithmetic_grpc {
Status MaxServiceImpl::Max(
    __attribute__((unused)) ServerContext* context_ptr,
    ServerReaderWriter<MaxResponse, MaxRequest>* stream_ptr) {
  std::cout << "Starting Max Service" << std::endl;
  std::int64_t max = INT64_MIN;
  MaxRequest current_request;
  while (stream_ptr->Read(&current_request)) {
    const auto number = current_request.number();
    std::cout << "Received number " << number << std::endl;
    if (arithmetic::UpdateMax(max, number)) {
      std::cout << "Max updated" << std::endl;
      MaxResponse response;
      response.set_max(max);
      stream_ptr->Write(response);
    } else {
      std::cout << "No update to max" << std::endl;
    }
  }
  std::cout << "Max Service completed" << std::endl;
  return Status::OK;
}

}  // namespace arithmetic_grpc
