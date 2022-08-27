#ifndef MAX_CLIENT_H_
#define MAX_CLIENT_H_

#include <arithmetic_proto/max.grpc.pb.h>
#include <grpc++/grpc++.h>

#include <cstdint>
#include <limits>
#include <memory>
#include <thread>
#include <utility>
#include <vector>

namespace arithmetic_grpc {

using arithmetic_proto::MaxService;

using grpc::Channel;

class MaxClient {
 public:
  MaxClient(std::shared_ptr<Channel> channel,
            std::uint64_t simulated_processing_time_ms = 200);
  std::pair<bool, std::int64_t> GetMax(
      const std::vector<std::int64_t>& numbers);
  static constexpr std::pair<bool, std::int64_t> MAX_FAILURE_MESSAGE{
      false, std::numeric_limits<std::int64_t>::quiet_NaN()};

 private:
  std::unique_ptr<MaxService::Stub> stub_ptr_;
  const std::uint64_t simulated_processing_time_ms_;
};

}  // namespace arithmetic_grpc

#endif
