import os

from hkpilot.Interfaces.Utilities.cmake import CMake

from hkpilot.Interfaces.Utilities.fancylogger import getLogger

logger = getLogger("hk-install")

import argparse

def print_hi():
    a_cmake = CMake("hk-eventDisplay", "/Users/mguigue/Work/T2K/HK/Software/newSystem/hk-eventDisplay")
    print(f'Hi, {a_cmake.package_name}')

    if not a_cmake.Configure():
        print("Error")

    if not a_cmake.Build():
        print("Error")

    if not a_cmake.Install():
        print("Error")


# function defined for setup_old.cfg
def main():

    parser = argparse.ArgumentParser(prog='hk-install')
    parser.add_argument('--version', action='store_true', help='Print version')

    sub_parsers = parser.add_subparsers(help='sub-command help')

    parser_ahoy = sub_parsers.add_parser('version', help='ahoy is cool sub-command')
    parser_ahoy.add_argument('--bar', type=int, help='bar is useful option')

    if not os.environ.get("HK_SYSTEM"):
        logger.error("Cannot find env variable HK_SYSTEM: please source hk-pilot/setup.sh; exiting...")
        exit(1)
    args = parser.parse_args()
    print(args)
    if args.version:
        print(args.version)

if __name__ == '__main__':
    main()
