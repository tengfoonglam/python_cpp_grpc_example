#include "arithmetic_grpc/sum_client.h"

#include <cmath>
#include <iostream>

using arithmetic_proto::SumRequest;
using arithmetic_proto::SumResponse;

using grpc::ClientContext;
using grpc::Status;

namespace arithmetic_grpc {

SumClient::SumClient(std::shared_ptr<Channel> channel)
    : stub_ptr_(SumService::NewStub(channel)) {}

float SumClient::Sum(float a, float b) {
  // Data we are sending to the server.
  SumRequest request;
  request.set_number_1(a);
  request.set_number_2(b);

  // Container for the data we expect from the server.
  SumResponse response;

  // Context for the client.
  // It could be used to convey extra information to the server and/or tweak
  // certain RPC behaviors.
  ClientContext context;

  // The actual RPC.
  const Status status = stub_ptr_->Sum(&context, request, &response);

  // Act upon its status.
  if (status.ok()) {
    return response.answer();
  } else {
    std::cout << "Sum service faild with error code " << status.error_code()
              << ": " << status.error_message() << std::endl;
    return std::nanf("");
  }
}

}  // namespace arithmetic_grpc
