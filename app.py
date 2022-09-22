
import datetime
from github import Github

from config import Configuration



def toDatetime(string):
    return datetime.datetime.strptime(string, "%a, %d %b %Y %H:%M:%S %Z")



def getNewestRepo(repos):
    newest_repo = None
    newest_commit = None
    for repo in repos:
        commit = repo.get_commits()[0]

        if (newest_commit == None): 
            newest_repo = repo
            newest_commit = commit

        if (toDatetime(commit.last_modified) > toDatetime(newest_commit.last_modified)):
            newest_repo = repo
            newest_commit = commit
    return newest_repo





g = Github(Configuration.GITHUB_ACCESS_TOKEN)

user = g.get_user()
repos = user.get_repos()

newest_repo = getNewestRepo(repos)
commits = newest_repo.get_commits()

# print ('\n\n')
print (newest_repo.name)
print (newest_repo.created_at)
print (commits[0].last_modified)




