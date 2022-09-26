


from github import Github
from core import app
from config import Configuration



if (__name__ != '__main__'):
    print ("Program Running")

    g = Github(Configuration.GITHUB_ACCESS_TOKEN)

    for repo in g.get_user().get_repos():
        print(repo.name)
        # print(dir(repo))
        break


if __name__ == '__main__':
    app.run()




