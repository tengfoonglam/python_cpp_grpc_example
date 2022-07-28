#include "arithmetic_grpc/average_client.h"

#include <cmath>
#include <iostream>

using namespace arithmetic_proto;

namespace arithmetic_grpc {

using grpc::Status;

AverageClient::AverageClient(std::shared_ptr<Channel> channel)
    : stub_ptr_(AverageService::NewStub(channel)) {}

bool AverageClient::AddNumber(const std::int32_t number) {
  bool success = false;

  if (!writer_ptr_) {
    context_ptr_ = new ClientContext();
    response_ptr_ = new AverageResponse();
    writer_ptr_ = stub_ptr_->Average(context_ptr_, response_ptr_);
  }

  AverageRequest request;
  request.set_number(number);

  if (writer_ptr_->Write(request)) {
    std::cout << "Added number " << number << " to be averaged" << std::endl;
    success = true;
  } else {
    std::cout << "Failed to add number, resetting client" << std::endl;
    Cleanup();
  }

  return success;
}

std::pair<bool, float> AverageClient::ComputeAverage() {
  std::pair<bool, float> output{false, 0.0f};

  if (writer_ptr_) {
    writer_ptr_->WritesDone();
    const auto status = writer_ptr_->Finish();
    if (status.ok()) {
      const auto answer = response_ptr_->answer();
      output = std::make_pair(true, answer);
      std::cout << "Average received from server: " << answer << std::endl;
    } else {
      std::cout
          << "Average client-side RPC streaming service failed with error code "
          << status.error_code() << ": " << status.error_message() << std::endl;
    }
    Cleanup();
  }

  return output;
}

void AverageClient::Cleanup() {
  if (writer_ptr_) {
    writer_ptr_.reset();
    delete context_ptr_;
    delete response_ptr_;
  }
}

AverageClient::~AverageClient() { Cleanup(); }

}  // namespace arithmetic_grpc
