from hkpilot.utils import fancylogger
from hkpilot.utils.buildtools import BuildTools
from hkpilot.utils.files import mkdir, read_dependencies_file

import multiprocessing
import subprocess
import os

logger = fancylogger.getLogger(__name__)


class MetaPackage(BuildTools):

    def __init__(self, path):
        super().__init__(path)
        self._type = "MetaPackage"
        self._cmake_options = dict()  # dictionary containing cmake options

    def check_dependencies(self):
        # self._depends_on.update(read_dependencies_file(os.path.join(self._path, self._cmakelist_path)))
        return True

    def configure(self):
        logger.info(f"Configuration of {self._package_name} in progress...")
        logger.info(f"Configuration of {self._package_name} done successfully")
        return True

    def build(self):
        logger.info(f"Build of {self._package_name} in progress...")
        logger.info(f"Build of {self._package_name} done successfully")
        return True

    def install(self):
        logger.info(f"Installation of {self._package_name} in progress...")
        logger.info(f"Installation of {self._package_name} done successfully")
        return True
