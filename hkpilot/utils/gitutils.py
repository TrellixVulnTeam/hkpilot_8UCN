from hkpilot.utils import fancylogger

logger = fancylogger.getLogger(__name__)

from git import Git, Repo
from git.exc import GitCommandError


def clone(git_url, path):
    logger.debug(f"Cloning {git_url} in {path}")
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


def find_commits_tags(path):
    repo = Repo(path)
    tagmap = {}
    for t in repo.tags:
        tagmap.setdefault(repo.commit(t), []).append(t)
    return tagmap


def find_commit_info(path):
    git = Git(path)
    try:
        desc = git.describe("--tags")
    except GitCommandError as a:
        logger.warn("Couldn't grab tags: setting version as 0.0.1")
        desc = "v0.0.1"
    if len(desc.split('-')) == 1:
        version = desc
        repo = Repo(path)
        sha = repo.head.object.hexsha[0:7]
        return version, "0", sha
    version = desc.split("-")[0]
    number_commit_ahead = int(desc.split("-")[1])
    commit_hash = desc.split("-")[2][1:]
    if number_commit_ahead > 0:
        logger.warn(f"Not on tag-commit: {commit_hash} is {number_commit_ahead} commit ahead")
    return version, number_commit_ahead, commit_hash
