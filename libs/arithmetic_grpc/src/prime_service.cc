#include "arithmetic_grpc/prime_service.h"

#include <arithmetic/arithmetic.h>

#include <cstdint>
#include <iostream>

using arithmetic_proto::PerformPrimeNumberDecompositionRequest;
using arithmetic_proto::PerformPrimeNumberDecompositionService;

using grpc::ServerContext;
using grpc::Status;

namespace arithmetic_grpc {

Status
PerformPrimeNumberDecompositionServiceImpl::PerformPrimeNumberDecomposition(
    __attribute__((unused)) ServerContext* context_ptr,
    const PerformPrimeNumberDecompositionRequest* request_ptr,
    ServerWriter<PerformPrimeNumberDecompositionResponse>*
        response_writer_ptr) {
  const auto number_to_process = request_ptr->number();
  const auto prime_numbers =
      arithmetic::GetPrimeNumberDecomposition(number_to_process);
  for (const auto prime_number : prime_numbers) {
    PerformPrimeNumberDecompositionResponse response;
    response.set_factor(prime_number);
    response_writer_ptr->Write(response);
  }
  return Status::OK;
}

}  // namespace arithmetic_grpc
