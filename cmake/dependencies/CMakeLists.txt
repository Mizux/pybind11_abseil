include(FetchContent)

# collect FetchContent_Declared components to make them available collectively below
set(DECLARED_CONTENTS "")

# abseil ================================================================================
option(BUILD_abseil "Fetch and build abseil" ON)
message(STATUS "Fetching and building abseil: ${BUILD_abseil}")
if(BUILD_abseil)
  # ensure that abseil also installs itself, since we are using it in our public API
  set(ABSL_ENABLE_INSTALL ON)
  set(ABSL_PROPAGATE_CXX_STD ON)
  set(BUILD_TESTING OFF)
  FetchContent_Declare(
    abseil-cpp
    URL https://github.com/abseil/abseil-cpp/archive/refs/tags/20230802.0.tar.gz
    URL_HASH
      SHA256=59d2976af9d6ecf001a81a35749a6e551a335b949d34918cfade07737b9d93c5
  )
  list(APPEND DECLARED_CONTENTS abseil-cpp)
endif()

# pybind11 ==============================================================================
option(BUILD_pybind11 "Fetch and build pybind11" ON)
message(STATUS "Fetching and building pybind11: ${BUILD_pybind11}")
if(BUILD_pybind11)
  FetchContent_Declare(
    pybind11
    URL https://github.com/pybind/pybind11/archive/refs/heads/master.tar.gz
  )
  list(APPEND DECLARED_CONTENTS pybind11)
endif()

if(DECLARED_CONTENTS)
  FetchContent_MakeAvailable(${DECLARED_CONTENTS})
endif()
