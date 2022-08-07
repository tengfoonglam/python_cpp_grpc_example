#ifndef ARITHMETIC_SUM_CLIENT_H_
#define ARITHMETIC_SUM_CLIENT_H_

#include <arithmetic_proto/sum.grpc.pb.h>
#include <grpc++/grpc++.h>

#include <memory>

namespace arithmetic_grpc {

using arithmetic_proto::SumService;
using grpc::Channel;

class SumClient {
 public:
  SumClient(std::shared_ptr<Channel> channel);
  float Sum(float a, float b);

 private:
  std::unique_ptr<SumService::Stub> stub_ptr_;
};

}  // namespace arithmetic_grpc

#endif
