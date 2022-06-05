#ifndef MAX_CLIENT_H_
#define MAX_CLIENT_H_

#include <arithmetic_proto/max.grpc.pb.h>
#include <grpc++/grpc++.h>

#include <memory>
#include <thread>
#include <utility>
#include <vector>

namespace arithmetic_grpc {

using arithmetic_proto::MaxService;

using grpc::Channel;

class MaxClient {
 public:
  MaxClient(std::shared_ptr<Channel> channel);
  std::pair<bool, std::int64_t> GetMax(
      const std::vector<std::int64_t>& numbers);

 private:
  std::unique_ptr<MaxService::Stub> stub_ptr_;
};

}  // namespace arithmetic_grpc

#endif
