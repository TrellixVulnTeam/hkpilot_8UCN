import os
from hkpilot.utils.fancylogger import getLogger
from hkpilot.utils.files import download, mkdir, unzip
from hkpilot.utils.gitutils import checkout_tag, checkout_branch, clone, find_commit_info

logger = getLogger(__name__)


class BuildTools(object):

    def __init__(self, path):
        self._type = "default"
        self._package_name = ""
        if path != "":
            self._path = path
        self._package_version, self._git_commit_ahead, self._git_commit_hash = find_commit_info(self._path)

        if os.environ.get("HK_SYSTEM"):
            self._hk_system = os.environ.get("HK_SYSTEM")
        else:
            logger.warn("HK_SYSTEM variable not provided!")
            self._hk_system = ""
        if self._hk_system != "":
            self._build_folder = os.path.join(self._path, f"build-{self._hk_system}")
            self._install_folder = os.path.join(self._path, f"install-{self._hk_system}")
        else:
            logger.warn("Using default folder pattern!")
            self._build_folder = os.path.join(self._path, "build")
            self._install_folder = os.path.join(self._path, "install")
        self._git_url = None
        self._download_url = None
        self._git_branch = None
        self._git_tag = None
        self._repo = None # Git repository
        self._n_procs = 0
        self._externals_src_dir = None
        self._depends_on = dict() # dictionary containing the dependencies of the package

    def print(self):
        log_string = f"\
    Package details:\n\
    Name: {self.package_name}\n\
    Version: {self.package_version} ({self._git_commit_ahead} ~ {self._git_commit_hash})\n\
    Installation type: {self.type}\n\
    External sources: {self.has_external_sources}"
        if self._git_url:
            log_string += f"\n    Git URL: {self._git_url}"
        if len(self._depends_on.items()) > 0:
            log_string += f"\n    Depends on:"
            for key, value in self._depends_on.items():
                log_string += f"\n    -> {key}: {value}"
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
    def n_procs(self):
        return self._n_procs

    @n_procs.setter
    def n_procs(self, value):
        self._n_procs = value

    @property
    def path(self):
        return self._path

    @property
    def package_name(self):
        return self._package_name

    @property
    def package_version(self):
        if self._package_version:
            return self._package_version
        print(find_tag(self._path))

    def check_dependencies(self):
        return True

    def download_source(self):
        if not self.has_external_sources:
            logger.debug("No external source to grab; moving on!")
            return True
        logger.info("Downloading external sources")
        if not self._externals_src_dir:
            logger.warning("Didn't provide a clone directory: cloning/downloading into tar/src")
            self._externals_src_dir = "src"
        if os.path.exists(os.path.join(self._path, self._cmakelist_path)):
            logger.warning(f"Source directory <{self._cmakelist_path}> already exists; cannot clone/download!")
        elif self._git_url:
            logger.debug("Cloning...")
            self._repo = clone(self._git_url, os.path.join(self._path, self._externals_src_dir))
        elif self._download_url:
            if not os.path.exists(os.path.join(self._path, "tar")):
                mkdir(os.path.join(self._path, "tar"))
            if self._download_url.endswith(".zip"):
                file = os.path.join(self._path, f"tar/{self.package_name}_{self.package_version}.zip")
            elif self._download_url.endswith(".tar.gz"):
                file = os.path.join(self._path, f"tar/{self.package_name}_{self.package_version}.tar.gz")
            else:
                logger.fatal(f"Unknown extension of URL: {self._download_url}; should be .zip or .tar.gz")
                exit(1)
            download(self._download_url, file)
            unzip(file, os.path.join(self._path, self._externals_src_dir))
            # logger.fatal("Not implemented yet!")
            # exit(1)
        else:
            logger.error("No git_url or download_url provided: nothing to download")
            return True

        if self._git_tag:
            checkout_tag(os.path.join(self._path, self._externals_src_dir), self._git_tag)
        elif self._git_branch:
            checkout_branch(os.path.join(self._path, self._externals_src_dir), self._git_branch)
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
