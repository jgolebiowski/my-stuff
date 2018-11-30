cmake_minimum_required(VERSION 3.7)
project(project_extension)

# Include pybinding
add_subdirectory(dependencies/pybind11)

# Gather all source files and define an executable
file(GLOB ${PROJECT_NAME}_src
        src/*.cpp
        bindings/*.cpp
        )

# Build as an executable or a library
pybind11_add_module(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_src})

# Add some libraries
#target_link_libraries(${PROJECT_NAME} -L/path/to/library)
#target_link_libraries(${PROJECT_NAME} -l{library_name})

# Include appropriate directories
target_include_directories(${PROJECT_NAME} PUBLIC src)
target_include_directories(${PROJECT_NAME} PUBLIC dependencies/include)
target_include_directories(${PROJECT_NAME} PUBLIC dependencies/Eigen)
#target_include_directories(${PROJECT_NAME} PUBLIC /path/to/include)


# Set cpp specifications
if(APPLE)
    set(CMAKE_CXX_COMPILER g++-7)
else()
    set(CMAKE_CXX_COMPILER g++)
endif()
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -Wextra -pedantic -fdiagnostics-color -Wno-cast-function-type -fopenmp -O3")
