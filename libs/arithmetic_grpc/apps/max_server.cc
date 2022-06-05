#include <arithmetic_grpc/grpc_utils.h>
#include <arithmetic_grpc/max_service.h>

#include <memory>
#include <string>

using namespace arithmetic_grpc;

int main(int argc, char** argv) {
  const std::vector<std::string> argumentList(argv + 1, argv + argc);
  const std::string address =
      (argumentList.size() == 1) ? argumentList.front() : DEFAULT_GRPC_ADDRESS;
  RunServer(address, std::make_unique<MaxServiceImpl>());
  return 0;
}
