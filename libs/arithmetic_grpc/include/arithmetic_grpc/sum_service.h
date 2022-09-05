#ifndef ARITHMETIC_SUM_SERVICE_H_
#define ARITHMETIC_SUM_SERVICE_H_

#include <arithmetic_proto/sum.grpc.pb.h>
#include <grpc++/grpc++.h>

#include <cstdint>

namespace arithmetic_grpc {

using arithmetic_proto::SumRequest;
using arithmetic_proto::SumResponse;
using arithmetic_proto::SumService;

using grpc::ServerContext;
using grpc::Status;

class SumServiceImpl final : public SumService::Service {
 public:
  SumServiceImpl(const std::uint64_t simulated_processing_time_ms = 200);

  Status Sum(__attribute__((unused)) ServerContext* context_ptr,
             const SumRequest* request_ptr, SumResponse* response_ptr) override;

 private:
  const std::uint64_t simulated_processing_time_ms_;
};

}  // namespace arithmetic_grpc

#endif
