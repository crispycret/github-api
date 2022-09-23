from github import Github
from core.utils import to_datetime


def get_repo_with_lastest_commit(repos):
    newest_repo = None
    newest_commit = None
    for repo in repos:
        commit = repo.get_commits()[0]

        if (newest_commit == None): 
            newest_repo = repo
            newest_commit = commit

        if (to_datetime(commit.last_modified) > to_datetime(newest_commit.last_modified)):
            newest_repo = repo
            newest_commit = commit
    return newest_repo



