#include <arithmetic_grpc/arithmetic_grpc.h>
#include <gtest/gtest.h>

#include <cmath>
#include <cstdint>
#include <memory>
#include <tuple>

using namespace arithmetic_grpc;

class AverageClientServerTests
    : public ::testing::TestWithParam<
          std::tuple<std::vector<std::int32_t>, float, bool>> {
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
  AverageServiceImpl service_;
  std::unique_ptr<Server> server_ptr_;
};

TEST_P(AverageClientServerTests, AverageNormalOperations) {
  const auto [numbers_to_average, answer, expected_success] = GetParam();
  AverageClient client(grpc::CreateChannel(DEFAULT_GRPC_ADDRESS,
                                           grpc::InsecureChannelCredentials()));
  for (const auto number : numbers_to_average) {
    client.AddNumber(number);
  }

  const auto& [success, output] = client.ComputeAverage();
  ASSERT_EQ(success, expected_success);
  ASSERT_FLOAT_EQ(output, answer);
}

INSTANTIATE_TEST_CASE_P(
    ArithmeticAverageGrpcTest, AverageClientServerTests,
    ::testing::Values(
        std::make_tuple(std::vector<std::int32_t>{}, 0.0f, false),
        std::make_tuple(std::vector<std::int32_t>{-1, 0, 1}, 0.0f, true),
        std::make_tuple(std::vector<std::int32_t>{1, 4}, 2.5f, true),
        std::make_tuple(std::vector<std::int32_t>{5, 10, 15, 20, 25}, 15.0f,
                        true),
        std::make_tuple(std::vector<std::int32_t>{-5, -10, -15, -20, -25},
                        -15.0f, true)));

TEST(ArithmeticAverageGrpcTest, AverageServerNotWorking) {
  AverageClient client(grpc::CreateChannel(DEFAULT_GRPC_ADDRESS,
                                           grpc::InsecureChannelCredentials()));
  ASSERT_FALSE(client.AddNumber(0));
  const auto& [success, output] = client.ComputeAverage();
  ASSERT_FALSE(success);
}
