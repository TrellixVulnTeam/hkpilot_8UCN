# GetVersionGit.cmake
# Author: M. Guigue
#
# Usage in top CMakeLists.txt: include GetVersionGit.cmake
#
# Extract the version using git
#
# Sets the following variables:
#   PROJECT_VERSION_MAJOR
#   PROJECT_VERSION_MINOR
#   PROJECT_REVISION

find_package( Git )
if( GIT_FOUND )

    execute_process(COMMAND ${GIT_EXECUTABLE} log --pretty=format:'%h' -n 1
            OUTPUT_VARIABLE GIT_REV
            ERROR_QUIET)
    # Check whether we got any revision (which isn't
    # always the case, e.g. when someone downloaded a zip
    # file from Github instead of a checkout)
    if ("${GIT_REV}" STREQUAL "")
        message(WARN "Failed retrieving info from git")
        set(GIT_REV "N/A")
        set(GIT_DIFF "")
        set(GIT_TAG "0.0.0")
        set(GIT_BRANCH "N/A")
    else()
        execute_process( COMMAND ${GIT_EXECUTABLE} remote get-url origin WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} OUTPUT_VARIABLE GIT_ORIGIN OUTPUT_STRIP_TRAILING_WHITESPACE )
        if( GIT_ORIGIN )
            message( STATUS "Git origin: ${GIT_ORIGIN}")
            string( REGEX MATCH "[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$" GIT_PACKAGE ${GIT_ORIGIN} )
        else( GIT_ORIGIN )
            execute_process( COMMAND ${GIT_EXECUTABLE} rev-parse --show-toplevel WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} OUTPUT_VARIABLE TOP_DIR OUTPUT_STRIP_TRAILING_WHITESPACE )
            execute_process( COMMAND basename ${TOP_DIR} OUTPUT_VARIABLE GIT_PACKAGE )
            message( STATUS "Git package: ${GIT_PACKAGE}" )
        endif( GIT_ORIGIN )

        execute_process(
                COMMAND ${GIT_EXECUTABLE} diff --quiet --exit-code
                WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                OUTPUT_VARIABLE ${PROJECT_NAME}_GIT_DIFF)
        execute_process(
                COMMAND ${GIT_EXECUTABLE} describe --exact-match --tags
                WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                OUTPUT_VARIABLE ${PROJECT_NAME}_GIT_TAG ERROR_QUIET)
        execute_process(
                COMMAND ${GIT_EXECUTABLE} rev-parse --abbrev-ref HEAD
                WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                OUTPUT_VARIABLE ${PROJECT_NAME}_GIT_BRANCH)

        string(STRIP "${${PROJECT_NAME}_GIT_REV}" ${PROJECT_NAME}_GIT_REV)
        string(SUBSTRING "${GIT_REV}" 1 7 GIT_REV)
        string(STRIP "${${PROJECT_NAME}_GIT_DIFF}" GIT_DIFF)
        string(STRIP "${${PROJECT_NAME}_GIT_TAG}" PROJECT_VERSION)
        string(STRIP "${${PROJECT_NAME}_GIT_BRANCH}" ${PROJECT_NAME}_GIT_BRANCH)
        message( STATUS "Git branch: ${${PROJECT_NAME}_GIT_BRANCH}" )
    endif()
endif( GIT_FOUND )

# Parse the version string into a list
string( REPLACE "." " " VERSION_SPACE_STRING ${PROJECT_VERSION} )
separate_arguments( VERSION_LIST UNIX_COMMAND ${VERSION_SPACE_STRING} )

# Put the version numbers into separate variables
list( GET VERSION_LIST 0 PROJECT_VERSION_MAJOR )
list( GET VERSION_LIST 1 PROJECT_VERSION_MINOR )
list( GET VERSION_LIST 2 PROJECT_REVISION )

message( STATUS "Git tag: ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_REVISION}")
