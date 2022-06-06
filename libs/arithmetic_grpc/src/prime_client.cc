#include "arithmetic_grpc/prime_client.h"

#include <cmath>
#include <iostream>

using arithmetic_proto::PerformPrimeNumberDecompositionRequest;
using arithmetic_proto::PerformPrimeNumberDecompositionResponse;

using grpc::ClientContext;
using grpc::ClientReader;
using grpc::Status;

namespace arithmetic_grpc {

PerformPrimeNumberDecompositionClient::PerformPrimeNumberDecompositionClient(
    std::shared_ptr<Channel> channel)
    : stub_ptr_(PerformPrimeNumberDecompositionService::NewStub(channel)) {}

std::vector<std::uint64_t>
PerformPrimeNumberDecompositionClient::PerformPrimeNumberDecomposition(
    std::uint64_t number) {
  std::vector<std::uint64_t> answer;

  PerformPrimeNumberDecompositionRequest request;
  request.set_number(number);

  ClientContext context;

  std::unique_ptr<ClientReader<PerformPrimeNumberDecompositionResponse>>
      reader_ptr(stub_ptr_->PerformPrimeNumberDecomposition(&context, request));

  PerformPrimeNumberDecompositionResponse response;

  std::cout << "Attempting to stream answer...";
  while (reader_ptr->Read(&response)) {
    answer.push_back(response.factor());
    std::cout << response.factor() << "...";
  }

  const Status status = reader_ptr->Finish();
  if (!status.ok()) {
    std::cout
        << "Prime decomposition server-side streaming failed with error code "
        << status.error_code() << ": " << status.error_message() << std::endl;
  } else {
    std::cout << "Prime decomposition server-side streaming completed"
              << std::endl;
  }

  return answer;
}

}  // namespace arithmetic_grpc
