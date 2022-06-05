#ifndef AVERAGE_SERVICE_H_
#define AVERAGE_SERVICE_H_

#include <arithmetic_proto/average.grpc.pb.h>
#include <arithmetic_proto/average.pb.h>
#include <grpc++/grpc++.h>

#include <cstdint>
#include <vector>

namespace arithmetic_grpc {

using arithmetic_proto::AverageRequest;
using arithmetic_proto::AverageResponse;
using arithmetic_proto::AverageService;

using grpc::ServerContext;
using grpc::ServerReader;
using grpc::Status;

class AverageServiceImpl final : public AverageService::Service {
 public:
  Status Average(__attribute__((unused)) ServerContext* context_ptr,
                 ServerReader<AverageRequest>* reader_ptr,
                 AverageResponse* response_ptr) override;
};

}  // namespace arithmetic_grpc
#endif
