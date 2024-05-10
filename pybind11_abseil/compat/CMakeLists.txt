# py_base_utilities ============================================================

add_library(py_base_utilities STATIC py_base_utilities.cc)
add_library(pybind11_abseil::compat::py_base_utilities ALIAS py_base_utilities)

target_include_directories(py_base_utilities
                           PUBLIC $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(py_base_utilities
                      PUBLIC absl::absl_check
                             absl::absl_log
                             absl::strings
                             absl::string_view
                             Python3::Module)

# status_from_core_py_exc ======================================================

add_library(status_from_core_py_exc STATIC status_from_core_py_exc.cc)
add_library(pybind11_abseil::compat::status_from_core_py_exc ALIAS
            status_from_core_py_exc)

target_include_directories(status_from_core_py_exc
                           PUBLIC $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(status_from_core_py_exc
                      PUBLIC py_base_utilities
                             absl::flat_hash_map
                             absl::status
                             Python3::Module)

# status_from_py_exc ===========================================================

add_library(status_from_py_exc STATIC status_from_py_exc.cc)
add_library(pybind11_abseil::compat::status_from_py_exc ALIAS
            status_from_py_exc)

target_include_directories(status_from_py_exc
                           PUBLIC $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(status_from_py_exc
                      PUBLIC py_base_utilities
                             status_from_core_py_exc
                             raw_ptr_from_capsule
                             absl::absl_check
                             absl::absl_log
                             absl::status
                             Python3::Module)
