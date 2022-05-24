from hkpilot.utils import fancylogger

logger = fancylogger.getLogger(__name__)


def checkout(repo, branch_name):
    logger.debug(f"Checking out {branch_name}")
    try:
        found_branch = False
        for branch in repo.branches:
            if branch.name == branch_name:
                logger.debug(f"Found {branch_name}")
                branch.checkout()
                found_branch = True
                break
        if not found_branch:
            logger.fatal("No branch with the right name")
            exit(1)
    except:
        logger.fatal(f"Error while checking out {branch_name}")
        exit(1)
    logger.debug(f"Check out successful")
