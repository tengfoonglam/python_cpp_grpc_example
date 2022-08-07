#include <arithmetic_grpc/grpc_utils.h>
#include <arithmetic_grpc/max_service.h>

#include <memory>
#include <string>

using namespace arithmetic_grpc;

int main(int argc, char** argv) {
  const std::vector<std::string> argument_list(argv + 1, argv + argc);
  const std::string address = (argument_list.size() == 1)
                                  ? argument_list.front()
                                  : DEFAULT_GRPC_ADDRESS;
  MaxServiceImpl service;
  CreateServerAndAttachServiceThenWait(address, &service);
  return 0;
}
