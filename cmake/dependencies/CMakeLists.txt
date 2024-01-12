include(FetchContent)
set(BUILD_TESTING OFF)

if(NOT TARGET absl::base)
  set(ABSL_PROPAGATE_CXX_STD ON)
  FetchContent_Declare(
    absl
    URL https://github.com/abseil/abseil-cpp/archive/refs/tags/20230802.0.tar.gz
    URL_HASH
    SHA256=59d2976af9d6ecf001a81a35749a6e551a335b949d34918cfade07737b9d93c5)
  FetchContent_MakeAvailable(absl)
endif()

if(NOT TARGET pybind11::pybind11_headers)
  FetchContent_Declare(
    pybind11
    URL https://github.com/pybind/pybind11/archive/refs/heads/master.tar.gz)
  FetchContent_MakeAvailable(pybind11)
endif()
