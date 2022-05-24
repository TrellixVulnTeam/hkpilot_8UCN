import os
import sys
import inspect
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
