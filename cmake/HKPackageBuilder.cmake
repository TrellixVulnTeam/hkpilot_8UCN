include(PackageBuilder)

function( hkbuilder_prepare_project )

    MESSAGE("Preparing project ${PROJECT_NAME} version ${PROJECT_VERSION}" )

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