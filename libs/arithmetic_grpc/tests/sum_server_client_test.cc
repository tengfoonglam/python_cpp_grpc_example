#include <arithmetic_grpc/arithmetic_grpc.h>
#include <gtest/gtest.h>

#include <cmath>
#include <cstdint>
#include <memory>

using namespace arithmetic_grpc;

class SumClientServerTests
    : public ::testing::TestWithParam<std::tuple<float, float, float>> {
 protected:
  void SetUp() {
    server_ptr_ = CreateServerAndAttachService(DEFAULT_GRPC_ADDRESS, &service_);
  }

  void TearDown() {
    if (server_ptr_) {
      const auto waitDuration = std::chrono::milliseconds(50);
      const auto deadline = std::chrono::system_clock::now() + waitDuration;
      server_ptr_->Shutdown(deadline);
    }
  }

 private:
  SumServiceImpl service_;
  std::unique_ptr<Server> server_ptr_;
};

TEST_P(SumClientServerTests, SumNormalOperations) {
  const auto& [number_1, number_2, answer] = GetParam();
  SumClient client(grpc::CreateChannel(DEFAULT_GRPC_ADDRESS,
                                       grpc::InsecureChannelCredentials()));
  const auto output = client.Sum(number_1, number_2);
  ASSERT_FLOAT_EQ(answer, output);
}

INSTANTIATE_TEST_CASE_P(ArithmeticGrpcSumTest, SumClientServerTests,
                        ::testing::Values(std::make_tuple(0, 0, 0),
                                          std::make_tuple(-1, -2, -3),
                                          std::make_tuple(1, 2, 3),
                                          std::make_tuple(1, -2, -1),
                                          std::make_tuple(-1, 2, 1)));

TEST(ArithmeticGrpcSumTest, SumServerNotWorking) {
  SumClient client(grpc::CreateChannel(DEFAULT_GRPC_ADDRESS,
                                       grpc::InsecureChannelCredentials()));
  const auto output = client.Sum(0, 0);
  ASSERT_TRUE(std::isnan(output));
}
