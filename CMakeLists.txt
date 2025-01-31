cmake_minimum_required(VERSION 3.30)
include(buildSettings.cmake)
project(${CURRENT_PROJECT_NAME} VERSION ${CURRENT_PROJECT_VERSION})

set(CMAKE_CXX_STANDARD 17)

# Определяем платформу
if(CMAKE_GENERATOR STREQUAL "MinGW Makefiles")
    set(CMAKE_BUILDING_PLATFORM "MinGW")
elseif(CMAKE_GENERATOR STREQUAL "Visual Studio 17 2022")
    set(CMAKE_BUILDING_PLATFORM "VS")
else()
    message(FATAL_ERROR "Неподдерживаемый генератор: ${CMAKE_GENERATOR}")
endif()

include_directories(
    ${CMAKE_SOURCE_DIR}/deps/${CMAKE_BUILDING_PLATFORM}/glfw/include
    ${CMAKE_SOURCE_DIR}/deps/${CMAKE_BUILDING_PLATFORM}/glew/include
)

link_directories(
    ${CMAKE_SOURCE_DIR}/deps/${CMAKE_BUILDING_PLATFORM}/glfw/lib
    ${CMAKE_SOURCE_DIR}/deps/${CMAKE_BUILDING_PLATFORM}/glew/lib
)

add_executable(${PROJECT_NAME} src/main.cpp)

if(CMAKE_BUILDING_PLATFORM STREQUAL "MinGW")
    target_link_libraries(${PROJECT_NAME} ${MINGW_LIBS})
elseif(CMAKE_BUILDING_PLATFORM STREQUAL "VS")
    target_link_libraries(${PROJECT_NAME} ${VS_LIBS})
endif()

# Опции сборки (отладочная/релизная)
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    # Добавить здесь опции отладки
else()
    # Добавить здесь опции релизной сборки
endif()