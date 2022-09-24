

import json
from github import Github
from flask import jsonify

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

    

@app.route('/repo_last_modified', methods=['GET'])
def repo_last_modified ():
    print('repo_last_modified')
    
    g = Github(Configuration.GITHUB_ACCESS_TOKEN)
    user = {}
    user['name'] = g.get_user().name

    # user = User.create_from_api(g.get_user())
    # return jsonify(user.serialize)

    return jsonify(user)
