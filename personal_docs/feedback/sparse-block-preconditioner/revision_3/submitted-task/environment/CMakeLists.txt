cmake_minimum_required(VERSION 3.16)
project(solverctl LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(solverctl
    src/main.cpp
    src/case_io.cpp
    csr_m/assemble.cpp
    bsr_n/layout.cpp
    perm_p/order.cpp
    prec_r/apply.cpp
    scale_q/metric.cpp
    solve_s/driver.cpp
    flow_t/report.cpp
    drive_u/run.cpp
    spill_v/bucket.cpp
    mirror_w/trace.cpp
)

target_include_directories(solverctl PRIVATE include)

set_target_properties(solverctl PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
