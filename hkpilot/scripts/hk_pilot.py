import os
import sys
import shutil

from hkpilot.utils.cmake import CMake
from hkpilot.utils.files import find_install_script, get_class, find_git_url
from hkpilot.utils.gitutils import clone

from hkpilot.utils.fancylogger import getLogger

logger = getLogger("hk-install")

import argparse


def print_hi():
    a_cmake = CMake("hk-eventDisplay", "/Users/mguigue/Work/T2K/HK/Software/newSystem/hk-eventDisplay")
    print(f'Hi, {a_cmake.package_name}')

    if not a_cmake.configure():
        print("Error")

    if not a_cmake.build():
        print("Error")

    if not a_cmake.install():
        print("Error")


def install_package(args):
    a_path = os.path.join(os.environ.get("HK_WORK_DIR"), args.name)
    logger.info(f"Installing {a_path}")
    # First check if folder already exists
    # If the folder doesn't exist, will try to grab it
    if not os.path.exists(a_path):
        logger.info(f"Package {a_path} doesn't exist; trying to clone")
        git_url = find_git_url(args.name)
        # find package in repos inventory
        clone(git_url, a_path)
    install_module_file = find_install_script(a_path)
    if install_module_file:
        logger.debug(f"Found non-empty install script: {install_module_file}")
    install_obj = get_class(install_module_file)(a_path)
    install_obj.print()
    install_obj.n_procs = args.j
    if not install_obj.download_source():
        logger.fatal("Error while downloading!")
        exit(1)
    install_obj.configure()
    install_obj.build()
    install_obj.install()
    return True


def clean_package(args):
    a_path = os.path.join(os.environ.get("HK_WORK_DIR"), args.name)
    logger.info(f"Cleaning {a_path}")
    if not os.path.exists(a_path):
        logger.info(f"Package {a_path} doesn't exist; nothing to clean")
        return False
    try:
        shutil.rmtree(os.path.join(a_path, os.environ.get("HK_PILOT_BUILD_PATTERN")))
    except FileNotFoundError:
        logger.warn("No build folder to remove")
    try:
        shutil.rmtree(os.path.join(a_path, "src"))
    except FileNotFoundError:
        logger.warn("No src folder to remove")
    try:
        shutil.rmtree(os.path.join(a_path, "tar"))
    except FileNotFoundError:
        logger.warn("No tar folder to remove")
    if args.deep:
        logger.info(f"Deep cleaning: removing install folder")
        try:
            shutil.rmtree(os.path.join(a_path, os.environ.get("HK_PILOT_INSTALL_PATTERN")))
        except FileNotFoundError:
            logger.warn("No install folder to remove")

    return True

def main():
    if not os.environ.get("HK_SYSTEM"):
        logger.fatal("Cannot find env variable HK_SYSTEM: please source hkpilot/setup.sh; exiting...")
        exit(1)

    parser = argparse.ArgumentParser(prog='hk-install')
    parser.add_argument('--version', action='store_true', help='Print version')
    parser.add_argument('--system', action='store_true', help='Print system path')

    sub_parsers = parser.add_subparsers(help='sub-command help')

    parser_install = sub_parsers.add_parser('install', help='Install a package')
    parser_install.add_argument('name', type=str, help='Package name/location')
    parser_install.add_argument('-j', type=int, help="Number of threads to use (default=3)", default=3)
    parser_install.set_defaults(func=install_package)

    parser_clean = sub_parsers.add_parser('clean', help='Clean a package')
    parser_clean.add_argument('name', type=str, help='Package name/location')
    parser_clean.add_argument('--deep', action='store_true', help="Also remove install folder")
    parser_clean.set_defaults(func=clean_package)


    args = parser.parse_args()

    print(args)
    if args.version:
        print(args.version)
        return
    elif args.system:
        print(os.environ.get("HK_SYSTEM"))
        return

    # try:
    if args.func:
        if not args.func(args):
            logger.fatal("Error!")
            exit(1)
    # except  AttributeError as e:
    #     print("No subcommand provided !")
    #     parser.print_help(sys.stderr)
    #     exit(1)


if __name__ == '__main__':
    main()
