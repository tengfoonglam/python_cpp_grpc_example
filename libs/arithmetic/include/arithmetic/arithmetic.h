#ifndef ARITHMETIC_H_
#define ARITHMETIC_H_

#include <numeric>
#include <vector>

namespace arithmetic {

template <typename IN>
inline float ComputeAverage(const std::vector<IN>& numbers) {
  if (numbers.empty()) {
    return 0.0f;
  }

  return static_cast<float>(std::accumulate(numbers.begin(), numbers.end(), 0) /
                            static_cast<float>(numbers.size()));
}

template <typename T>
inline bool UpdateMax(T& current_max, const T& value_to_check) {
  bool max_updated = false;
  if (current_max < value_to_check) {
    current_max = value_to_check;
    max_updated = true;
  }
  return max_updated;
}

template <typename T,
          class = typename std::enable_if<std::is_unsigned<T>::value>::type>
inline std::vector<T> GetPrimeNumberDecomposition(T number) {
  std::vector<T> answer;
  T divisor = 2;
  while (number > 1) {
    if (number % divisor == 0) {
      number /= divisor;
      answer.push_back(divisor);
    } else {
      divisor++;
    }
  }
  return answer;
}

template <typename T>
inline T Sum(T number_1, T number_2) {
  return number_1 + number_2;
}

}  // namespace arithmetic

#endif