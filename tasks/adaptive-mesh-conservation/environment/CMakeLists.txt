cmake_minimum_required(VERSION 3.16)
project(sim_run LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(NOT DEFINED BUILD_STAMP)
    if(DEFINED ENV{SOURCE_DATE_EPOCH})
        set(BUILD_STAMP $ENV{SOURCE_DATE_EPOCH})
    else()
        set(BUILD_STAMP "0")
    endif()
endif()
add_compile_definitions(BUILD_STAMP=${BUILD_STAMP})

add_executable(sim_run
    src/main.cpp
    src/case_io.cpp
    src/vault_io.cpp
    src/audit_emit.cpp
    acc_m/edge_corr.cpp
    lnk_n/relate.cpp
    agg_q/blend.cpp
    srl_p/serial.cpp
    rsm_k/resume.cpp
    sync_b/halo.cpp
    drv_u/run.cpp
    drv_u/run_refine.cpp
    drv_u/run_blend.cpp
    drv_u/run_sync.cpp
    swp_t/sweep.cpp
    emt_e/report.cpp
    prb_v/hist.cpp
    tap_w/trace.cpp
    cch_z/ring.cpp
)

target_include_directories(sim_run PRIVATE include)

set_target_properties(sim_run PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
