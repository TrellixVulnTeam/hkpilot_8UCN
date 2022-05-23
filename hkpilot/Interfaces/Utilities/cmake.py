from hkpilot.Interfaces.Utilities import fancylogger
from hkpilot.Interfaces.Utilities.buildtools import BuildTools
from hkpilot.Interfaces.Utilities.files import mkdir

import subprocess
import os
from git import Repo

logger = fancylogger.getLogger(__name__)


class CMake(BuildTools):

    def __init__(self, name, path):
        super().__init__(name, path)
        self._type = "CMake"
        self._build_folder = os.path.join(self._path, "build")
        self._install_folder = os.path.join(self._path, "install")

    def Download(self):
        Repo.clone_from(git_url, repo_dir)


    def Configure(self):
        logger.info(f"Configuration of {self._package_name} in progress...")
        cmake_file = os.path.join(self._path, "CMakeLists.txt")
        if not os.path.exists(cmake_file):
            logger.error(f"Cannot find CMakeLists.txt in {self._path}")
            return False

        mkdir(self._build_folder)  ## TODO make nicer (using os path and gcc version)
        mkdir(self._install_folder)  ## TODO make nicer (using os path and gcc version)

        cmake_cmd = f"cmake -D CMAKE_INSTALL_PREFIX={self._install_folder} -S {self._path} -B {self._build_folder}"
        logger.debug(f"Running <{cmake_cmd}>")
        retCode = subprocess.check_call([cmake_cmd], stderr=subprocess.STDOUT, shell=True)
        if retCode == 0:
            logger.info(f"Configuration of {self._package_name} done successfully")
            return True
        logger.error(f"Configuration of {self._package_name} failed!")
        return False

    def Build(self):
        logger.info(f"Build of {self._package_name} in progress...")

        cmakeCmd = f"cmake --build {self._build_folder}"
        logger.debug(f"Running <{cmakeCmd}>")
        retCode = subprocess.check_call([cmakeCmd], stderr=subprocess.STDOUT, shell=True)
        if retCode == 0:
            logger.info(f"Configuration of {self._package_name} done successfully")
            return True
        logger.error(f"Configuration of {self._package_name} failed!")
        return False

    def Install(self):
        logger.info(f"Installation of {self._package_name} in progress...")

        cmakeCmd = f"cmake --build {self._build_folder} --target install"
        logger.debug(f"Running <{cmakeCmd}>")
        retCode = subprocess.check_call([cmakeCmd], stderr=subprocess.STDOUT, shell=True)
        if retCode == 0:
            logger.info(f"Installation of {self._package_name} done successfully")
            return True
        logger.error(f"Installation of {self._package_name} failed!")
        return False
