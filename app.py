



from github import Github
from core import app
from config import Configuration

if __name__ == '__main__':

 
    g = Github(Configuration.GITHUB_ACCESS_TOKEN, base_url="https://github.company.com/api/v3")
    print (g)
    print(g.get_user())
    print(g.get_user('crispycret'))
    print(g.get_user('crispycret').name)
    # print(g.get_user().email)
    # user = {}
    # user['name'] = g.get_user('').name

    # app.run()




