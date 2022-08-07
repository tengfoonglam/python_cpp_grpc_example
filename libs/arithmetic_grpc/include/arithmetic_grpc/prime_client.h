#ifndef ARITHMETIC_PRIME_CLIENT_H_
#define ARITHMETIC_PRIME_CLIENT_H_

#include <arithmetic_proto/prime.grpc.pb.h>
#include <grpc++/grpc++.h>

#include <cstdint>
#include <memory>
#include <vector>

namespace arithmetic_grpc {

using arithmetic_proto::PerformPrimeNumberDecompositionService;
using grpc::Channel;

class PerformPrimeNumberDecompositionClient {
 public:
  PerformPrimeNumberDecompositionClient(std::shared_ptr<Channel> channel);
  std::vector<std::uint64_t> PerformPrimeNumberDecomposition(
      std::uint64_t number);

 private:
  std::unique_ptr<PerformPrimeNumberDecompositionService::Stub> stub_ptr_;
};

}  // namespace arithmetic_grpc

#endif
