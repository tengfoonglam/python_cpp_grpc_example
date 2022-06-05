#ifndef AVERAGE_CLIENT_H_
#define AVERAGE_CLIENT_H_

#include <arithmetic_proto/average.grpc.pb.h>
#include <grpc++/grpc++.h>

#include <cstdint>
#include <memory>
#include <utility>
#include <vector>

namespace arithmetic_grpc {

using arithmetic_proto::AverageRequest;
using arithmetic_proto::AverageResponse;
using arithmetic_proto::AverageService;
using grpc::Channel;
using grpc::ClientContext;
using grpc::ClientWriter;

class AverageClient {
 public:
  AverageClient(std::shared_ptr<Channel> channel);
  bool AddNumber(std::int32_t number);
  std::pair<bool, float> ComputeAverage();
  ~AverageClient();

  AverageClient(const AverageClient& other) = delete;
  AverageClient& operator=(AverageClient const&) = delete;

 private:
  std::unique_ptr<AverageService::Stub> stub_ptr_;
  std::unique_ptr<ClientWriter<AverageRequest>> writer_ptr_;
  ClientContext* context_ptr_;
  AverageResponse* response_ptr_;
};

}  // namespace arithmetic_grpc

#endif
