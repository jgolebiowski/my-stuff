cmake_minimum_required(VERSION 3.10)
project(sample_project)

# Gather all source files and define an executable
file(GLOB ${PROJECT_NAME}_src
        src/*.cpp
        )

# Build as an executable or a library
add_executable(${PROJECT_NAME} ${${PROJECT_NAME}_src})
#add_library(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_src})

# Add some libraries
#target_link_libraries(${PROJECT_NAME} -L/usr/lib)
#target_link_libraries(${PROJECT_NAME} -lm)

# Include appropriate directories
target_include_directories(${PROJECT_NAME} PUBLIC src)
target_include_directories(${PROJECT_NAME} PUBLIC /Users/golejace/Documents/eigen-git-mirror)


# Set cpp specifications
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_COMPILER g++-8)
set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -Wextra -pedantic -Wno-cast-function-type -O3 -fopenmp -fdiagnostics-color")

# Move binaries to a specified location
#set(OUTPUT_DIR "/Users/golejace/Documents/coding-workspace/cpp-school/sample_project_1/build")
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_DIR})
#set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${OUTPUT_DIR})
#set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${OUTPUT_DIR})
#
#set(EXECUTABLE_OUTPUT_PATH ${OUTPUT_DIR})
#set(LIBRARY_OUTPUT_PATH ${OUTPUT_DIR})