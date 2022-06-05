#ifndef ARITHMETIC_PRIME_SERVICE_H_
#define ARITHMETIC_PRIME_SERVICE_H_

#include <arithmetic_proto/prime.grpc.pb.h>
#include <grpc++/grpc++.h>

#include <cstdint>

namespace arithmetic_grpc {

using arithmetic_proto::PerformPrimeNumberDecompositionRequest;
using arithmetic_proto::PerformPrimeNumberDecompositionResponse;
using arithmetic_proto::PerformPrimeNumberDecompositionService;
using grpc::ServerContext;
using grpc::ServerWriter;
using grpc::Status;

class PerformPrimeNumberDecompositionServiceImpl final
    : public PerformPrimeNumberDecompositionService::Service {
 public:
  Status PerformPrimeNumberDecomposition(
      __attribute__((unused)) ServerContext* context_ptr,
      const PerformPrimeNumberDecompositionRequest* request_ptr,
      ServerWriter<PerformPrimeNumberDecompositionResponse>*
          response_writer_ptr) override;
};

}  // namespace arithmetic_grpc

#endif
