
set( SET_INSTALL_PREFIX_TO_DEFAULT OFF CACHE BOOL "Reset default install path when when configuring" FORCE  )
include(PackageBuilder)



function( hkbuilder_prepare_project )
    set(default_build_type "Release")
    if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
        message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
        set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
                STRING "Choose the type of build." FORCE)
        # Set the possible values of build type for cmake-gui
        set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
                "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
    endif ()

    pbuilder_prepare_project()


    configure_file(${PROJECT_SOURCE_DIR}/${PROJECT_NAME}Config.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake @ONLY)
    pbuilder_do_package_config()

    add_custom_target(install_${PROJECT_NAME}
            "${CMAKE_COMMAND}" --build "${CMAKE_BINARY_DIR}" --target install
            COMMENT "Installing ${PROJECT_NAME}")


endfunction()

function ( hk_package NAME VERSION)
    # This function tries to make sure a package is properly installed.
    # The check procedure either uses the presence of the <package_name>Config.cmake file or XXX for Makefile based installation.
    #
    # Parameters:
    #     NAME: package name
    #     VERSION: package version
    #     PATH (optional):

    set (A_PATH "/Users/mguigue/Work/T2K/HK/Software/newSystem/myhkdep/install-$ENV{HK_SYSTEM}")
    set (CMAKE_FIND_FRAMEWORK "LAST")
    set (CMAKE_FIND_APPBUNDLE  "LAST")
    if("${VERSION}" STREQUAL "*")
        message(STATUS "No specific version required for ${NAME}")
        find_package( myhkdep PATHS ${A_PATH} REQUIRED)
    else()
        message(STATUS "Version ${VERSION} required for ${NAME}")
        find_package( myhkdep PATHS ${A_PATH} VERSION ${VERSION} REQUIRED)
    endif()

    set (extra_args ${ARGN})

endfunction(hk_package)

function ( hk_check_dependencies )
    # Make sure we have the VERSION file
    find_file( DEPENDENCIES_FILE "dependencies.cmake" ${CMAKE_CURRENT_SOURCE_DIR} NO_DEFAULT_PATH )
    if( NOT EXISTS ${DEPENDENCIES_FILE} )
        message( FATAL_ERROR "Did not find dependencies.cmake file" )
    endif()
    include(${DEPENDENCIES_FILE})
endfunction( hk_check_dependencies )