import os
import sys

from hkpilot.utils.cmake import CMake
from hkpilot.utils.files import find_install_script, get_class

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
    a_path = args.path
    logger.info(f"Installing {a_path}")
    install_module_file = find_install_script(a_path)
    if install_module_file:
        logger.debug(f"Found non-empty install script: {install_module_file}")
    install_obj = get_class(install_module_file)(a_path)
    print(install_obj.path)
    logger.info(f"Test {a_path}")
    install_obj.print()
    print(args.download)
    if args.download:
        logger.info("Downloading package...")
        if not install_obj.download():
            logger.fatal("Error while downloading!")
            exit(1)
    install_obj.configure()
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
    parser_install.add_argument('path', type=str, help='Package name/location')
    parser_install.add_argument('--download', action='store_true', help='Download package before installation')
    parser_install.set_defaults(func=install_package)

    args = parser.parse_args()
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
