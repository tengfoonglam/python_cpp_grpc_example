#include <arithmetic_grpc/arithmetic_grpc.h>
#include <gtest/gtest.h>

#include <cmath>
#include <cstdint>
#include <limits>
#include <memory>
#include <tuple>
#include <vector>

using namespace arithmetic_grpc;

class MaxClientServerTests
    : public ::testing::TestWithParam<
          std::tuple<std::vector<std::int64_t>, bool, std::int64_t>> {
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
  MaxServiceImpl service_;
  std::unique_ptr<Server> server_ptr_;
};

TEST_P(MaxClientServerTests, MaxNormalOperations) {
  const auto [numbers_to_max, expected_success, answer] = GetParam();
  MaxClient client(grpc::CreateChannel(DEFAULT_GRPC_ADDRESS,
                                       grpc::InsecureChannelCredentials()));
  const auto [success, output] = client.GetMax(numbers_to_max);
  ASSERT_EQ(success, expected_success);
  ASSERT_EQ(output, answer);
}

INSTANTIATE_TEST_CASE_P(
    ArithmeticMaxGrpcTest, MaxClientServerTests,
    ::testing::Values(
        std::make_tuple(std::vector<std::int64_t>{},
                        MaxClient::MAX_FAILURE_MESSAGE.first,
                        MaxClient::MAX_FAILURE_MESSAGE.second),
        std::make_tuple(std::vector<std::int64_t>{0, 1, 3}, true, 3),
        std::make_tuple(std::vector<std::int64_t>{-1, 0, 10, 10, 80, 88}, true,
                        88),
        std::make_tuple(std::vector<std::int64_t>{88, 80, 10, 10, 0, -1}, true,
                        88),
        std::make_tuple(std::vector<std::int64_t>{-5, -10, -15, -20, -25}, true,
                        -5),
        std::make_tuple(std::vector<std::int64_t>{-25, -20, -15, -10, -5}, true,
                        -5),
        std::make_tuple(
            std::vector<std::int64_t>{MaxClient::MAX_FAILURE_MESSAGE.second},
            true, MaxClient::MAX_FAILURE_MESSAGE.second)));

TEST(ArithmeticMaxGrpcTest, MaxServerNotWorking) {
  MaxClient client(grpc::CreateChannel(DEFAULT_GRPC_ADDRESS,
                                       grpc::InsecureChannelCredentials()));
  const std::vector<std::int64_t> valid_input{0, 1, 3};
  const auto [success, output] = client.GetMax(valid_input);
  ASSERT_FALSE(success);
}
