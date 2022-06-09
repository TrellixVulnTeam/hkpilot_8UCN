import inspect
import os
import sys
from urllib import request
import yaml
import zipfile

from hkpilot.utils.fancylogger import getLogger
import importlib.util

logger = getLogger(__name__)


def mkdir(path):
    if os.path.exists(path):
        return
    os.makedirs(path)


def find_install_script(path):
    if not os.path.exists(path):
        logger.fatal(f"Request path <{path}> don't exist!")
        exit(1)
    if not os.path.exists(os.path.join(path, "hkinstall.py")):
        logger.fatal(f"Cannot find hkinstall.py script in <{path}>!")
        exit(1)
    return os.path.join(path, "hkinstall.py")


def get_class(file):
    import imp
    foo = imp.load_source('module', file)

    import module
    for name, obj in inspect.getmembers(sys.modules['module']):
        if inspect.isclass(obj):
            a_string = str(obj)
            if "module." in a_string:
                logger.debug(f"Creating object of {name}")
                return obj
    logger.fatal(f"Couldn't find class in {file}")
    exit(1)


def find_git_url(name):
    a_path = os.path.join(os.environ.get("HK_PILOT_DIR"), "data/repos.yaml")
    if not os.path.exists(a_path):
        logger.fatal(f"No such {a_path}")
        exit(1)
    with open(a_path, "r") as stream:
        try:
            a_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.fatal(exc)
            exit(1)
        if name in a_dict["repos"]:
            logger.debug(f"Found URL for {name}: {a_dict['repos'][name]}")
            return a_dict['repos'][name]


def download(url, path):
    logger.info(f"Downloading {url} into {path}")
    response = request.urlretrieve(url, path)


def unzip(path_to_zip_file, where_to_unzip):
    logger.info(f"Unziping {path_to_zip_file} to {where_to_unzip}")
    if not os.path.exists(path_to_zip_file):
        logger.fatal("File to unzip doesn't exist")
        exit(1)
    if not os.path.exists(where_to_unzip):
        logger.warning("Directory where to unzip doesn't exist, creating it!")
        mkdir(where_to_unzip)
        # exit(1)
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(where_to_unzip)