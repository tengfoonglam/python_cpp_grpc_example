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

const std::string DEFAULT_GRPC_ADDRESS{"0.0.0.0:50051"};

void inline RunServer(const std::string& address,
                      std::unique_ptr<grpc::Service> service_ptr) {
  grpc::EnableDefaultHealthCheckService(true);
  grpc::reflection::InitProtoReflectionServerBuilderPlugin();
  ServerBuilder builder;
  builder.AddListeningPort(address, grpc::InsecureServerCredentials());
  builder.RegisterService(service_ptr.release());
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << address << std::endl;
  server->Wait();
}

}  // namespace arithmetic_grpc
#endif
