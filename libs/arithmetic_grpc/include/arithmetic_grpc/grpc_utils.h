#ifndef GRPC_UTILS_H_
#define GRPC_UTILS_H_

#include <arithmetic_grpc/prime_service.h>
#include <grpc++/grpc++.h>
#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/health_check_service_interface.h>

#include <memory>
#include <string>
#include <vector>

namespace arithmetic_grpc {

using grpc::Server;
using grpc::ServerBuilder;
using grpc::Service;

const std::string DEFAULT_GRPC_ADDRESS{"0.0.0.0:50051"};

std::unique_ptr<Server> inline CreateServerAndAttachServices(
    const std::string& address, const std::vector<Service*>& service_ptrs) {
  grpc::EnableDefaultHealthCheckService(true);
  grpc::reflection::InitProtoReflectionServerBuilderPlugin();
  ServerBuilder builder;
  builder.AddListeningPort(address, grpc::InsecureServerCredentials());
  for (const auto& service_ptr : service_ptrs) {
    builder.RegisterService(service_ptr);
  }
  std::unique_ptr<Server> server_ptr(builder.BuildAndStart());
  std::cout << "Server listening on " << address << std::endl;
  return server_ptr;
}

std::unique_ptr<Server> inline CreateServerAndAttachService(
    const std::string& address, Service* service_ptr) {
  const std::vector<Service*> input{service_ptr};
  return CreateServerAndAttachServices(address, input);
}

void inline CreateServerAndAttachServicesThenWait(
    const std::string& address, const std::vector<Service*>& service_ptrs) {
  auto server_ptr = CreateServerAndAttachServices(address, service_ptrs);
  server_ptr->Wait();
}

void inline CreateServerAndAttachServiceThenWait(const std::string& address,
                                                 Service* service_ptr) {
  auto server_ptr = CreateServerAndAttachService(address, service_ptr);
  server_ptr->Wait();
}

}  // namespace arithmetic_grpc
#endif
