find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

if(NOT BUILD_abseil)
  find_package(absl REQUIRED)
endif()

if(NOT BUILD_pybind11)
  find_package(pybind11 REQUIRED)
endif()
