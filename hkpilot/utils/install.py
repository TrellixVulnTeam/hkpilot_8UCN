# All installation procedures

from hkpilot.utils.fancylogger import getLogger

logger = getLogger(__name__)


def do_install(install_obj, *args, **kwargs):
    install_obj.print()
    install_obj.n_procs = kwargs.j if "j" in kwargs else 0
    if not install_obj.download_source():
        logger.fatal("Error while downloading!")
        exit(1)
    if not install_obj.configure():
        return False
    if not install_obj.build():
        return False
    if not install_obj.install():
        return False
    return True


def do_recursive_install(install_obj, *args, **kwargs):
    install_obj.check_dependencies()
    for key, value in install_obj._depends_on.items():
        print(key)
        rec_install_obj = get_install_class(install_module_file)(a_path)
    return True
