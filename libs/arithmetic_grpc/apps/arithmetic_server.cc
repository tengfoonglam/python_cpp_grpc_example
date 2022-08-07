#include <arithmetic_grpc/arithmetic_grpc.h>
#include <arithmetic_grpc/grpc_utils.h>

#include <memory>
#include <string>

using namespace arithmetic_grpc;

int main(int argc, char** argv) {
  const std::vector<std::string> argument_list(argv + 1, argv + argc);
  const std::string address = (argument_list.size() == 1)
                                  ? argument_list.front()
                                  : DEFAULT_GRPC_ADDRESS;
  AverageServiceImpl average_service;
  MaxServiceImpl max_service;
  PerformPrimeNumberDecompositionServiceImpl prime_service;
  SumServiceImpl averge_service;

  CreateServerAndAttachServicesThenWait(
      address,
      {&average_service, &max_service, &prime_service, &averge_service});
  return 0;
}
