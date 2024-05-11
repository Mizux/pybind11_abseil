# void_ptr_from_capsule ========================================================

add_library(void_ptr_from_capsule STATIC void_ptr_from_capsule.cc)
add_library(pybind11_abseil::cpp_capsule_tools::void_ptr_from_capsule ALIAS
            void_ptr_from_capsule)

target_include_directories(void_ptr_from_capsule
                           PUBLIC $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(void_ptr_from_capsule
                      PUBLIC absl::statusor
                             Python3::Module
                      PRIVATE absl::status
                              absl::strings)

# raw_ptr_from_capsule =========================================================

add_library(raw_ptr_from_capsule INTERFACE)
add_library(pybind11_abseil::cpp_capsule_tools::raw_ptr_from_capsule ALIAS
            raw_ptr_from_capsule)

target_include_directories(raw_ptr_from_capsule
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(raw_ptr_from_capsule
                      INTERFACE void_ptr_from_capsule
                                absl::statusor
                                Python3::Module)

# make_shared_ptr_capsule ======================================================

add_library(make_shared_ptr_capsule INTERFACE)
add_library(pybind11_abseil::cpp_capsule_tools::make_shared_ptr_capsule ALIAS
            make_shared_ptr_capsule)

target_include_directories(make_shared_ptr_capsule
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(make_shared_ptr_capsule
                      INTERFACE Python3::Module)

# shared_ptr_from_capsule ======================================================

add_library(shared_ptr_from_capsule INTERFACE)
add_library(pybind11_abseil::cpp_capsule_tools::shared_ptr_from_capsule ALIAS
            shared_ptr_from_capsule)

target_include_directories(shared_ptr_from_capsule
                           INTERFACE $<BUILD_INTERFACE:${TOP_LEVEL_DIR}>
                                     $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_link_libraries(shared_ptr_from_capsule
                      INTERFACE void_ptr_from_capsule
                                absl::statusor
                                Python3::Module)

install(
    TARGETS
      void_ptr_from_capsule
      raw_ptr_from_capsule
      make_shared_ptr_capsule
      shared_ptr_from_capsule
    EXPORT
      pybind11_abseilTargets
    INCLUDES
      DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    RUNTIME
      DESTINATION ${CMAKE_INSTALL_BINDIR}
      COMPONENT pybind11_abseil_Runtime
    LIBRARY
      DESTINATION ${CMAKE_INSTALL_LIBDIR}
      COMPONENT pybind11_abseil_Runtime
      NAMELINK_COMPONENT pybind11_abseil_Development
    ARCHIVE
      DESTINATION ${CMAKE_INSTALL_LIBDIR}
      COMPONENT pybind11_abseil_Development
)

install(
  FILES
    make_shared_ptr_capsule.h
    raw_ptr_from_capsule.h
    shared_ptr_from_capsule.h
    void_ptr_from_capsule.h
  DESTINATION
    "${CMAKE_INSTALL_INCLUDEDIR}/pybind11_abseil/cpp_capsule_tools"
)