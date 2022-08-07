#ifndef MAX_SERVICE_H_
#define MAX_SERVICE_H_

#include <arithmetic_proto/max.grpc.pb.h>
#include <grpc++/grpc++.h>

#include <cstdint>
#include <vector>

namespace arithmetic_grpc {

using arithmetic_proto::MaxRequest;
using arithmetic_proto::MaxResponse;
using arithmetic_proto::MaxService;

using grpc::ServerContext;
using grpc::ServerReaderWriter;
using grpc::Status;

class MaxServiceImpl final : public MaxService::Service {
 public:
  Status Max(__attribute__((unused)) ServerContext* context_ptr,
             ServerReaderWriter<MaxResponse, MaxRequest>* stream_ptr) override;
};

}  // namespace arithmetic_grpc
#endif
