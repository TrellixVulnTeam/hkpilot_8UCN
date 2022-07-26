import inspect
import os
import sys
from urllib import request
import yaml
import zipfile
import tarfile

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


def get_install_class(file):
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
    if path_to_zip_file.endswith(".zip"):
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(where_to_unzip)
    elif path_to_zip_file.endswith(".tar.gz"):
        with tarfile.open(path_to_zip_file) as tar_ref:
            tar_ref.extractall(where_to_unzip)
    else:
        logger.fatal("Unknown extension")
        exit(1)



def read_dependencies_file(path):
    logger.debug(f"Defining additional dependencies from <{path}>")
    if not os.path.exists(path):
        logger.warning(f"Dependency path <{path}> doesn't exist; exiting!")
        return dict()
    if not os.path.exists(os.path.join(path, "dependencies.cmake")):
        logger.warn(f"Cannot find dependencies.cmake in <{path}>; skipping...")
        return dict()
    file_path = os.path.join(path, "dependencies.cmake")
    a_dict = dict()
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("#"):
                logger.debug(f"Skipping line {line}")
                continue
            if not "hk_package" in line:
                logger.warn(f"Skipping {line}")
                logger.warn("Make sure the line is 'hk_package( <package_name> <package_version>)'")
                continue
            a_list = line[line.find("(")+len("("):line.rfind(")")].split()
            if len(a_list) < 2:
                logger.warn("Not enough arguments in line")
                logger.warn("Make sure the line is 'hk_package( <package_name> <package_version>)'")
                continue
            logger.info(f"Requires {str(a_list[0])} ({str(a_list[1])})")
            a_dict.update({str(a_list[0]): str(a_list[1])})
    return a_dict

