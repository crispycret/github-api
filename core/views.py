

import json
from github import Github

from config import Configuration

from core import app
from core.common import get_repo_with_lastest_commit
from core.models import User, Repo, Commit

@app.route('/', methods=['GET'])
def test():
    print('test')
    return {'status': 200}

@app.route('/update')
def update ():
    '''
        Retrieve all supported data from the Github API and store
        in a relation database for faster queries.
    '''
    g = Github(Configuration.GITHUB_ACCESS_TOKEN)
    user = User.create_from_api(g.get_user())

    

@app.route('/last_modified_repo', methods=['GET'])
def last_modified_repo ():
    print('last_modified_repo')
    
    g = Github(Configuration.GITHUB_ACCESS_TOKEN)

    user = g.get_user()
    repos = user.get_repos()


    newest_repo = get_repo_with_lastest_commit(repos)
    commits = newest_repo.get_commits()

    newest_repo.default_branch
    newest_repo.html_url

    # print ('\n\n')
    print (newest_repo.name)
    print (newest_repo.created_at)
    print (commits[0].last_modified)
    results = json.dumps(newest_repo)
    return results
