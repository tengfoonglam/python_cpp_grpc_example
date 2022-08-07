#include "arithmetic_grpc/max_service.h"

#include <arithmetic/arithmetic.h>

#include <cstdint>
#include <iostream>

namespace arithmetic_grpc {
Status MaxServiceImpl::Max(
    __attribute__((unused)) ServerContext* context_ptr,
    ServerReaderWriter<MaxResponse, MaxRequest>* stream_ptr) {
  std::int64_t max = INT64_MIN;
  MaxRequest current_request;
  while (stream_ptr->Read(&current_request)) {
    if (arithmetic::UpdateMax(max, current_request.number())) {
      MaxResponse response;
      response.set_max(max);
      stream_ptr->Write(response);
    }
  }
  return Status::OK;
}

}  // namespace arithmetic_grpc
