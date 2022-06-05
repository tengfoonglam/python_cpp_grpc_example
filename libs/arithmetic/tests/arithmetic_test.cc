#include <arithmetic/arithmetic.h>
#include <gtest/gtest.h>

#include <cstdint>
#include <vector>

// Disclaimer: This is by no means an exhaustive list of tests, just some sanity
// checks

using namespace arithmetic;

class ComputeAverageTests : public ::testing::TestWithParam<
                                std::pair<std::vector<std::int64_t>, float>> {};

TEST_P(ComputeAverageTests, ComputeAverage) {
  const auto& [input, answer] = GetParam();
  const auto output = ComputeAverage(input);
  ASSERT_FLOAT_EQ(answer, output);
}

INSTANTIATE_TEST_CASE_P(
    ArithmeticTest, ComputeAverageTests,
    ::testing::Values(
        std::make_pair(std::vector<std::int64_t>{}, 0.0f),
        std::make_pair(std::vector<std::int64_t>{-1, 0, 1}, 0.0f),
        std::make_pair(std::vector<std::int64_t>{1, 4}, 2.5f),
        std::make_pair(std::vector<std::int64_t>{5, 10, 15, 20, 25}, 15.0f),
        std::make_pair(std::vector<std::int64_t>{-5, -10, -15, -20, -25},
                       -15.0f)));

class ComputeUpdateMaxTests
    : public ::testing::TestWithParam<std::tuple<float, float, bool>> {};

TEST_P(ComputeUpdateMaxTests, UpdateMax) {
  const auto& [starting_max, value_to_check, max_updated_answer] = GetParam();
  auto max = starting_max;
  const auto max_updated = UpdateMax(max, value_to_check);
  ASSERT_EQ(max_updated, max_updated_answer);
  if (max_updated_answer) {
    ASSERT_FLOAT_EQ(max, value_to_check);
  } else {
    ASSERT_FLOAT_EQ(max, starting_max);
  }
}

INSTANTIATE_TEST_CASE_P(ArithmeticTest, ComputeUpdateMaxTests,
                        ::testing::Values(std::make_tuple(0.0f, 0.0f, false),
                                          std::make_tuple(-10.0f, 10.0f, true),
                                          std::make_tuple(5.0f, 10.0f, true),
                                          std::make_tuple(5.0f, -10.0f,
                                                          false)));

class GetPrimeNumberDecompositionTests
    : public ::testing::TestWithParam<
          std::pair<std::uint64_t, std::vector<std::uint64_t>>> {};

TEST_P(GetPrimeNumberDecompositionTests, GetPrimeNumberDecomposition) {
  const auto& [number_to_decompose, answer] = GetParam();
  const auto output = GetPrimeNumberDecomposition(number_to_decompose);
  ASSERT_EQ(output, answer);
}

INSTANTIATE_TEST_CASE_P(
    ArithmeticTest, GetPrimeNumberDecompositionTests,
    ::testing::Values(
        std::make_pair(0, std::vector<std::uint64_t>{}),
        std::make_pair(999, std::vector<std::uint64_t>{3, 3, 3, 37}),
        std::make_pair(3125, std::vector<std::uint64_t>{5, 5, 5, 5, 5}),
        std::make_pair(30030, std::vector<std::uint64_t>{2, 3, 5, 7, 11, 13}),
        std::make_pair(1265102983, std::vector<std::uint64_t>{2099, 602717})));

class SumTests : public ::testing::TestWithParam<
                     std::tuple<std::int64_t, std::int64_t, std::int64_t>> {};

TEST_P(SumTests, Sum) {
  const auto& [number_1, number_2, answer] = GetParam();
  const auto sum = Sum(number_1, number_2);
  ASSERT_EQ(sum, answer);
}

INSTANTIATE_TEST_CASE_P(ArithmeticTest, SumTests,
                        ::testing::Values(std::make_tuple(0, 0, 0),
                                          std::make_tuple(-1, -2, -3),
                                          std::make_tuple(1, 2, 3),
                                          std::make_tuple(1, -2, -1),
                                          std::make_tuple(-1, 2, 1)));
