from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup

from pathlib import Path
import os
import sys
import platform
import subprocess

# from hkpilot.utils.fancylogger import getLogger

# logger = getLogger("Install")

# logger.info("Starting installation of hk-pilot package")

hk_pilot_path = Path().absolute()
# logger.debug(f"File      Path: {Path(__file__).absolute()}" )
# logger.debug(f"Directory Path: {hk_pilot_path}")

python_version = platform.python_version()
python_mainversion = f"{sys.version_info.major}.{sys.version_info.minor}"
gcc_version = subprocess.run(["gcc", "-dumpversion"], stdout=subprocess.PIPE).stdout.decode("utf-8").splitlines()[0] #; gcc -"])
os_version = subprocess.run(["uname"], stdout=subprocess.PIPE).stdout.decode("utf-8").splitlines()[0] #; gcc -"])
arch = subprocess.run(["uname", "-m"], stdout=subprocess.PIPE).stdout.decode("utf-8").splitlines()[0] #; gcc -"])
# logger.info(f"Found OS: {os_version}-{arch}")
# logger.info(f"Found gcc version: {gcc_version}")
# logger.info(f"Found python version: {python_version}")

system_variable = f"{os_version}_{arch}-gcc_{gcc_version}-python_{python_version}"
# logger.debug(f"System variable: {system_variable}")

# Produce setup.sh from setup.sh.in
fin = open(os.path.join(hk_pilot_path, "setup.sh.in"), "rt")
fout = open(os.path.join(hk_pilot_path, "setup.sh"), "wt")
for line in fin:
    fout.write(line.replace('@HK_PILOT_DIR@', str(hk_pilot_path))
               .replace('@PYTHON_VERSION@', str(python_version))
               .replace('@PYTHON_MAINVERSION@', str(python_mainversion))
               .replace('@ARCH@', str(arch))
               .replace('@GCC_VERSION@', str(gcc_version))
               .replace('@OS@', str(os_version))
               .replace('@HK_SYSTEM@', str(system_variable))
               )
fin.close()
fout.close()


# This is required to allow editable pip installs while using the declarative configuration (setup.cfg)
setup()
