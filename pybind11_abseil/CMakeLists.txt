add_subdirectory(compat)
add_subdirectory(cpp_capsule_tools)

# absl_casters ============================================================
add_library(absl_casters INTERFACE)
add_library(pybind11_abseil::absl_casters ALIAS absl_casters)

target_include_directories(absl_casters
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(
  absl_casters
  INTERFACE absl::cleanup
            absl::btree
            absl::flat_hash_map
            absl::flat_hash_set
            absl::node_hash_map
            absl::node_hash_set
            absl::strings
            absl::time
            absl::optional
            absl::span
            pybind11::module)

# ok_status_singleton_lib ======================================================

add_library(ok_status_singleton_lib STATIC ok_status_singleton_lib.cc)
add_library(pybind11_abseil::ok_status_singleton_lib ALIAS
            ok_status_singleton_lib)

target_include_directories(ok_status_singleton_lib
                           PUBLIC $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(ok_status_singleton_lib
                      PUBLIC absl::status
                             Python3::Module)

# ok_status_singleton_pyinit_google3 ===========================================

add_library(ok_status_singleton_pyinit_google3 STATIC
            ok_status_singleton_pyinit_google3.cc)

target_link_libraries(ok_status_singleton_pyinit_google3
                      PUBLIC ok_status_singleton_lib
                             Python3::Module)

# ok_status_singleton =======================================================

pybind11_add_module(ok_status_singleton MODULE ok_status_singleton_py_extension_stub.cc)
add_library(pybind11_abseil::ok_status_singleton ALIAS ok_status_singleton)

# note: macOS is APPLE and also UNIX !
if(APPLE)
  set_target_properties(ok_status_singleton PROPERTIES SUFFIX ".so")
  set_property(TARGET ok_status_singleton APPEND PROPERTY
    LINK_FLAGS "-flat_namespace -undefined suppress")
endif()

target_include_directories(ok_status_singleton
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(ok_status_singleton
                      PUBLIC ok_status_singleton_pyinit_google3)

# no_throw_status ==============================================================

add_library(no_throw_status INTERFACE)
add_library(pybind11_abseil::no_throw_status ALIAS no_throw_status)

target_include_directories(no_throw_status
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

# status_not_ok_exception ======================================================

add_library(status_not_ok_exception INTERFACE)
add_library(pybind11_abseil::status_not_ok_exception ALIAS
            status_not_ok_exception)

target_include_directories(status_not_ok_exception
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(status_not_ok_exception INTERFACE absl::status)

# check_status_module_imported =================================================

add_library(check_status_module_imported INTERFACE)

target_include_directories(check_status_module_imported
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(check_status_module_imported
                      INTERFACE absl::status
                                pybind11::module)

# status_caster ================================================================

add_library(status_caster INTERFACE)
add_library(pybind11_abseil::status_caster ALIAS status_caster)

target_include_directories(status_caster
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(
  status_caster
  INTERFACE check_status_module_imported
            no_throw_status
            ok_status_singleton_lib
            status_from_py_exc
            status_not_ok_exception
            raw_ptr_from_capsule
            absl::status
            absl::statusor
            pybind11::module)

# statusor_caster ==============================================================

add_library(statusor_caster INTERFACE)
add_library(pybind11_abseil::statusor_caster ALIAS statusor_caster)

target_include_directories(statusor_caster
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(
  statusor_caster
  INTERFACE check_status_module_imported
            no_throw_status
            status_caster
            status_from_py_exc
            absl::status
            absl::statusor
            pybind11::module)

# init_from_tag ================================================================

add_library(init_from_tag INTERFACE)
add_library(pybind11_abseil::init_from_tag ALIAS init_from_tag)

target_include_directories(init_from_tag
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

# utils_pybind11_absl ==========================================================

pybind11_add_module(utils_pybind11_absl STATIC utils_pybind11_absl.cc)

target_include_directories(utils_pybind11_absl
                           PUBLIC $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(utils_pybind11_absl
                      PUBLIC absl::strings)

# register_status_bindings =====================================================

pybind11_add_module(register_status_bindings STATIC register_status_bindings.cc)

target_include_directories(register_status_bindings
                           PUBLIC $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(
  register_status_bindings
  PUBLIC absl_casters
         init_from_tag
         no_throw_status
         ok_status_singleton_lib
         status_caster
         status_not_ok_exception
         utils_pybind11_absl
         raw_ptr_from_capsule
         absl::status
         absl::statusor
         absl::strings)

# status_pyinit_google3 ========================================================

pybind11_add_module(status_pyinit_google3 STATIC status_pyinit_google3.cc)

target_link_libraries(status_pyinit_google3
                      PUBLIC register_status_bindings)

# status ====================================================================

pybind11_add_module(status_py_extension_stub MODULE status_py_extension_stub.cc)
add_library(pybind11_abseil::status ALIAS status_py_extension_stub)

set_target_properties(status_py_extension_stub PROPERTIES LIBRARY_OUTPUT_NAME "status")
# note: macOS is APPLE and also UNIX !
if(APPLE)
  set_target_properties(status_py_extension_stub PROPERTIES SUFFIX ".so")
  set_property(TARGET status_py_extension_stub APPEND PROPERTY
    LINK_FLAGS "-flat_namespace -undefined suppress")
endif()

set_target_properties(status_py_extension_stub PROPERTIES PREFIX "")

target_link_libraries(status_py_extension_stub
                      PUBLIC status_pyinit_google3
                              absl::status)

# import_status_module =========================================================

pybind11_add_module(import_status_module STATIC import_status_module.cc)
add_library(pybind11_abseil::import_status_module ALIAS import_status_module)

target_include_directories(import_status_module
                           PUBLIC $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

add_dependencies(import_status_module status_py_extension_stub)

# status_casters ===============================================================

add_library(status_casters INTERFACE)
add_library(pybind11_abseil::status_casters ALIAS status_casters)

target_include_directories(status_casters
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(status_casters
                      INTERFACE import_status_module
                                status_caster
                                statusor_caster)

if(BUILD_TESTING)
  add_subdirectory(tests)
endif()

if(CMAKE_INSTALL_PYDIR)
  # Copying to two target directories for simplicity. It is currently unknown
  # how to determine here which copy is actually being used.
  install(
    TARGETS status_py_extension_stub ok_status_singleton
    EXPORT pybind11_abseilTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_PYDIR}/pybind11_abseil
    ARCHIVE DESTINATION ${CMAKE_INSTALL_PYDIR}/pybind11_abseil
    RUNTIME DESTINATION ${CMAKE_INSTALL_PYDIR}/pybind11_abseil)

  install(
    TARGETS status_py_extension_stub ok_status_singleton
    EXPORT pybind11_abseil_cppTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR})

endif()
