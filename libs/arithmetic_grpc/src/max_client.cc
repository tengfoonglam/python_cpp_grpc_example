#include "arithmetic_grpc/max_client.h"

#include <chrono>
#include <limits>
#include <memory>
#include <thread>

using namespace arithmetic_proto;

using arithmetic_proto::MaxRequest;
using arithmetic_proto::MaxResponse;
using grpc::ClientContext;
using grpc::ClientReaderWriter;
using grpc::Status;

namespace arithmetic_grpc {

MaxClient::MaxClient(std::shared_ptr<Channel> channel)
    : stub_ptr_(MaxService::NewStub(channel)) {}

std::pair<bool, std::int64_t> MaxClient::GetMax(
    const std::vector<std::int64_t>& numbers) {
  std::pair<bool, std::int64_t> output{
      false, std::numeric_limits<std::int64_t>::quiet_NaN()};

  // This was adapted from official Routing Guide Client Example
  // Source:
  // https://github.com/grpc/grpc/blob/v1.45.0/examples/cpp/route_guide/route_guide_client.cc
  // For synchronous gRPC Read() is a blocking function so it is difficult
  // produce truly thread-safe code when you read and write at the same time
  // during bi-directional streaming

  ClientContext context;
  std::shared_ptr<ClientReaderWriter<MaxRequest, MaxResponse>> stream_ptr =
      stub_ptr_->Max(&context);

  std::thread writer([stream_ptr, numbers]() {
    for (const auto number : numbers) {
      std::cout << "Sending number to be maxed: " << number << std::endl;
      MaxRequest request;
      request.set_number(number);
      stream_ptr->Write(request);
      std::this_thread::sleep_for(std::chrono::milliseconds(
          250));  // So you can see sequence of requests and responses more
                  // clearly
    }
    stream_ptr->WritesDone();
  });

  MaxResponse response;
  while (stream_ptr->Read(&response)) {
    const auto max = response.max();
    output.second = max;
    output.first = true;
    std::cout << "Recevied new max: " << max << std::endl;
  }

  writer.join();

  Status status = stream_ptr->Finish();
  if (!status.ok()) {
    output.first = false;
    std::cout << "Max bi-direction RPC service failed with error code "
              << status.error_code() << ": " << status.error_message()
              << std::endl;
  } else {
    std::cout << "Final max: " << output.second << std::endl;
  }

  return output;
}
}  // namespace arithmetic_grpc
