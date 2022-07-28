#include <arithmetic_grpc/arithmetic_grpc.h>
#include <gtest/gtest.h>

#include <cmath>
#include <cstdint>
#include <memory>

using namespace arithmetic_grpc;

class PrimeClientServerTests
    : public ::testing::TestWithParam<
          std::pair<std::uint64_t, std::vector<std::uint64_t>>> {
 protected:
  void SetUp() {
    server_ptr_ = CreateServerAndAttachService(DEFAULT_GRPC_ADDRESS, service_);
  }

  void TearDown() {
    if (server_ptr_) {
      const auto waitDuration = std::chrono::milliseconds(50);
      const auto deadline = std::chrono::system_clock::now() + waitDuration;
      server_ptr_->Shutdown(deadline);
    }
  }

 private:
  PerformPrimeNumberDecompositionServiceImpl service_;
  std::unique_ptr<Server> server_ptr_;
};

TEST_P(PrimeClientServerTests, PrimeNormalOperations) {
  const auto& [number_to_decompose, answer] = GetParam();
  PerformPrimeNumberDecompositionClient client(grpc::CreateChannel(
      DEFAULT_GRPC_ADDRESS, grpc::InsecureChannelCredentials()));
  const auto output =
      client.PerformPrimeNumberDecomposition(number_to_decompose);
  ASSERT_EQ(answer, output);
}

INSTANTIATE_TEST_CASE_P(
    ArithmeticPrimeGrpcTest, PrimeClientServerTests,
    ::testing::Values(
        std::make_pair(0, std::vector<std::uint64_t>{}),
        std::make_pair(999, std::vector<std::uint64_t>{3, 3, 3, 37}),
        std::make_pair(3125, std::vector<std::uint64_t>{5, 5, 5, 5, 5}),
        std::make_pair(30030, std::vector<std::uint64_t>{2, 3, 5, 7, 11, 13}),
        std::make_pair(1265102983, std::vector<std::uint64_t>{2099, 602717})));

TEST(ArithmeticPrimeGrpcTest, PrimeServerNotWorking) {
  PerformPrimeNumberDecompositionClient client(grpc::CreateChannel(
      DEFAULT_GRPC_ADDRESS, grpc::InsecureChannelCredentials()));
  const auto output = client.PerformPrimeNumberDecomposition(3);
  ASSERT_TRUE(output.empty());
}
