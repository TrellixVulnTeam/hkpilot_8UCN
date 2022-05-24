import os

from hkpilot.utils.fancylogger import getLogger

logger = getLogger(__name__)

class BuildTools(object):

    def __init__(self, path):
        self._type = "default"
        self._package_name = ""
        self._package_version = None
        if path != "":
            self._path = path

        if os.environ.get("HK_SYSTEM"):
            self._hk_system = os.environ.get("HK_SYSTEM")
        else:
            logger.warn("HK_SYSTEM variable not provided!")
            self._hk_system = ""

    def print(self):
        logger.info(f"Package details:\n\
    Name: {self._package_name}\n\
    Version: {self._package_version}\n\
    Installaton type: {self._type}")

    @property
    def type(self):
        return self._type

    @property
    def path(self):
        return self._path

    @property
    def package_name(self):
        return self._package_name

    def download(self):
        return True

    def patch(self):
        return True

    def configure(self):
        return True

    def build(self):
        return True

    def install(self):
        return True

    def post_install(self):
        return True

    def check(self):
        return False

