from hkpilot.utils import fancylogger
from hkpilot.utils.buildtools import BuildTools
from hkpilot.utils.files import mkdir
from hkpilot.utils.gitutils import checkout

import subprocess
import os
from git import Repo
from git.exc import GitCommandError

logger = fancylogger.getLogger(__name__)


class CMake(BuildTools):

    def __init__(self, path):
        super().__init__(path)
        # self._git_branch_tag = None
        # self._git_clone_dir = None
        # self._git_url = None
        self._repo = None
        self._type = "CMake"
        if self._hk_system != "":
            self._build_folder = os.path.join(self._path, f"build-{self._hk_system}")
            self._install_folder = os.path.join(self._path, f"install-{self._hk_system}")
        else:
            logger.warn("Using default folder pattern!")
            self._build_folder = os.path.join(self._path, "build")
            self._install_folder = os.path.join(self._path, "install")

    def download(self):
        # if os.path.exists(os.path.join(self._path, self._git_clone_dir)):
        #     logger.fatal(f"Directory <{self._git_clone_dir}> already exists; cannot clone!")
        #     exit(1)
        if self._git_url and self._git_clone_dir and self._git_branch_tag:
            # logger.debug("Cloning...")
            # try:
            #     self._repo = Repo.clone_from(self._git_url, os.path.join(self._path, self._git_clone_dir))
            #
            # except GitCommandError as error:
            #     logger.fatal(f"Failed cloning and checkout:\n{error.stderr}")
            #     exit(1)
            # try:
            self._repo = Repo(os.path.join(self._path, self._git_clone_dir))
            logger.debug(f"Active branch: {self._repo.active_branch}")
            if self._repo.active_branch != self._git_branch_tag:
                checkout(self._repo, self._git_branch_tag)


            # except:
            #     logger.fatal("Error")
            #     exit(1)
            # branch = self._repo.active_branch
            # print(branch.name)
            # self._repo.git.checkout(self._git_branch_tag)
        else:
            logger.error("No git_url or clone_dir or _git_branch_tag provided")
            return False
        return True

    def configure(self):
        logger.info(f"Configuration of {self._package_name} in progress...")
        cmake_file = os.path.join(self.path, "CMakeLists.txt")
        if not os.path.exists(cmake_file):
            logger.error(f"Cannot find CMakeLists.txt in {self.path}")
            return False

        mkdir(self._build_folder)  # TODO make nicer (using os path and gcc version)
        mkdir(self._install_folder)  # TODO make nicer (using os path and gcc version)

        cmake_cmd = f"cmake -D CMAKE_INSTALL_PREFIX={self._install_folder} -S {self._path} -B {self._build_folder}"
        logger.debug(f"Running <{cmake_cmd}>")
        ret_code = subprocess.check_call([cmake_cmd], stderr=subprocess.STDOUT, shell=True)
        if ret_code == 0:
            logger.info(f"Configuration of {self._package_name} done successfully")
            return True
        logger.error(f"Configuration of {self._package_name} failed!")
        return False

    def build(self):
        logger.info(f"Build of {self._package_name} in progress...")

        cmake_cmd = f"cmake --build {self._build_folder}"
        logger.debug(f"Running <{cmake_cmd}>")
        ret_code = subprocess.check_call([cmake_cmd], stderr=subprocess.STDOUT, shell=True)
        if ret_code == 0:
            logger.info(f"Configuration of {self._package_name} done successfully")
            return True
        logger.error(f"Configuration of {self._package_name} failed!")
        return False

    def install(self):
        logger.info(f"Installation of {self._package_name} in progress...")

        cmake_cmd = f"cmake --build {self._build_folder} --target install"
        logger.debug(f"Running <{cmake_cmd}>")
        ret_code = subprocess.check_call([cmake_cmd], stderr=subprocess.STDOUT, shell=True)
        if ret_code == 0:
            logger.info(f"Installation of {self._package_name} done successfully")
            return True
        logger.error(f"Installation of {self._package_name} failed!")
        return False
