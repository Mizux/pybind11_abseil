include(FetchContent)

set(ABSL_PROPAGATE_CXX_STD ON)
set(BUILD_TESTING OFF)
FetchContent_Declare(
  abseil-cpp
  URL https://github.com/abseil/abseil-cpp/archive/refs/tags/20230802.0.tar.gz
  URL_HASH
    SHA256=59d2976af9d6ecf001a81a35749a6e551a335b949d34918cfade07737b9d93c5)

FetchContent_Declare(
  pybind11
  URL https://github.com/pybind/pybind11/archive/refs/heads/master.tar.gz)

FetchContent_MakeAvailable(abseil-cpp pybind11)
