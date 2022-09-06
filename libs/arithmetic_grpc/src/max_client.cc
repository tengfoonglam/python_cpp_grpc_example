#include "arithmetic_grpc/max_client.h"

#include <chrono>
#include <memory>
#include <thread>

using namespace arithmetic_proto;

namespace arithmetic_grpc {

using arithmetic_proto::MaxRequest;
using arithmetic_proto::MaxResponse;
using grpc::ClientContext;
using grpc::ClientReaderWriter;
using grpc::Status;

MaxClient::MaxClient(std::shared_ptr<Channel> channel,
                     std::uint64_t simulated_processing_time_ms)
    : stub_ptr_(MaxService::NewStub(channel)),
      simulated_processing_time_ms_(simulated_processing_time_ms) {}

std::pair<bool, std::int64_t> MaxClient::GetMax(
    const std::vector<std::int64_t>& numbers) {
  auto output = MAX_FAILURE_MESSAGE;

  // Guard clause: If empty vector provided as input, return immediately
  if (numbers.empty()) {
    return output;
  }

  // This was adapted from official Routing Guide Client Example
  // Source:
  // https://github.com/grpc/grpc/blob/v1.45.0/examples/cpp/route_guide/route_guide_client.cc
  // For synchronous gRPC Read() is a blocking function so it is difficult
  // produce truly thread-safe code when you read and write at the same time
  // during bi-directional streaming. This is because if you use a lock to
  // protect the Writer during Read() which blocks, it will not be available to
  // Write()

  ClientContext context;
  std::shared_ptr<ClientReaderWriter<MaxRequest, MaxResponse>> stream_ptr =
      stub_ptr_->Max(&context);

  // Write requests in a separate thread
  std::thread writer(
      [stream_ptr](const std::uint64_t simulated_processing_time_ms,
                   const std::vector<std::int64_t>& numbers) {
        for (const auto number : numbers) {
          std::cout << "Sending number to be maxed: " << number << std::endl;
          MaxRequest request;
          request.set_number(number);
          stream_ptr->Write(request);
          std::this_thread::sleep_for(std::chrono::milliseconds(
              simulated_processing_time_ms));  // So you can see sequence of
                                               // requests and responses
                                               // interlace more clearly
        }
        std::cout << "All writing completed" << std::endl;
        stream_ptr->WritesDone();
      },
      simulated_processing_time_ms_, numbers);

  // Receive and print out reponses while requests are being sent out
  std::this_thread::sleep_for(std::chrono::milliseconds(
      50));  // Give some time for writer to write data before starting to read
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
