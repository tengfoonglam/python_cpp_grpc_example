#ifndef ARITHMETIC_SUM_SERVICE_H_
#define ARITHMETIC_SUM_SERVICE_H_

#include <arithmetic_proto/sum.grpc.pb.h>
#include <grpc++/grpc++.h>

namespace arithmetic_grpc {

using arithmetic_proto::SumRequest;
using arithmetic_proto::SumResponse;
using arithmetic_proto::SumService;

using grpc::ServerContext;
using grpc::Status;

class SumServiceImpl final : public SumService::Service {
 public:
  Status Sum(__attribute__((unused)) ServerContext* context_ptr,
             const SumRequest* request_ptr, SumResponse* response_ptr) override;
};

}  // namespace arithmetic_grpc

#endif
