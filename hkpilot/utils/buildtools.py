import os
from hkpilot.utils.fancylogger import getLogger
from hkpilot.utils.gitutils import checkout_tag, checkout_branch, clone

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
        self._git_url = None
        self._git_branch = None
        self._git_tag = None

    def print(self):
        log_string = f"Package details:\n\
    Name: {self._package_name}\n\
    Version: {self._package_version}\n\
    Installation type: {self._type}\n\
    External sources: {self.has_external_sources}"
        if self._git_url:
            log_string += f"\n    Git URL: {self._git_url}"
        logger.info(log_string)

    @property
    def has_external_sources(self):
        if self._git_url or self._download_url:
            return True
        return False

    @property
    def type(self):
        return self._type

    @property
    def path(self):
        return self._path

    @property
    def package_name(self):
        return self._package_name

    def download_source(self):
        if not self.has_external_sources:
            logger.debug("No external source to grab; moving on!")
            return True
        logger.info("Downloading external sources")
        if not self._git_clone_dir:
            logger.fatal("Didn't provide a clone directory: exit")
            exit(1)
        if os.path.exists(os.path.join(self._path, self._git_clone_dir)):
            logger.warning(f"Directory <{self._git_clone_dir}> already exists; cannot clone/download!")
            # exit(1)
        elif self._git_url:
            logger.debug("Cloning...")
            self._repo = clone(self._git_url, os.path.join(self._path, self._git_clone_dir))
        elif self._download_url:
            logger.fatal("Not implemented yet!")
        else:
            logger.error("No git_url or download_url provided: nothing to download")
            return True

        if self._git_tag:
            checkout_tag(os.path.join(self._path, self._git_clone_dir), self._git_tag)
        elif self._git_branch:
            checkout_branch(os.path.join(self._path, self._git_clone_dir), self._git_branch)
        else:
            logger.warn("No tag or branch to checkout")
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
