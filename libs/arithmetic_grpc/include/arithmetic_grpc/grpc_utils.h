#ifndef GRPC_UTILS_H_
#define GRPC_UTILS_H_

#include <arithmetic_grpc/prime_service.h>
#include <grpc++/grpc++.h>
#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/health_check_service_interface.h>

#include <memory>
#include <string>

namespace arithmetic_grpc {

using grpc::Server;
using grpc::ServerBuilder;
using grpc::Service;

const std::string DEFAULT_GRPC_ADDRESS{"0.0.0.0:50051"};

std::unique_ptr<Server> inline CreateServerAndAttachService(
    const std::string& address, Service& service) {
  grpc::EnableDefaultHealthCheckService(true);
  grpc::reflection::InitProtoReflectionServerBuilderPlugin();
  ServerBuilder builder;
  builder.AddListeningPort(address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<Server> server_ptr(builder.BuildAndStart());
  std::cout << "Server listening on " << address << std::endl;
  return server_ptr;
}

void inline CreateServerAndAttachServiceThenWait(const std::string& address,
                                                 Service& service) {
  auto server_ptr = CreateServerAndAttachService(address, service);
  server_ptr->Wait();
}

}  // namespace arithmetic_grpc
#endif
