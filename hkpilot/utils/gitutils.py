from hkpilot.utils import fancylogger

logger = fancylogger.getLogger(__name__)

import os
from git import Repo
from git.exc import GitCommandError


def clone(git_url, path):
    try:
        repo = Repo.clone_from(git_url, path)
    except GitCommandError as error:
        logger.fatal(f"Failed cloning and checkout:\n{error.stderr}")
        exit(1)


def checkout_tag(path, tag_name):
    logger.fatal("Not implemented")
    exit(1)

def checkout_branch(path, branch_name):
    logger.debug(f"Checking out {branch_name} in {path}")
    repo = Repo(path)
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
