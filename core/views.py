

import json
from github import Github
from flask import jsonify

from config import Configuration

from core import app
from core.common import get_repo_with_lastest_commit
from core.models import User, Repo, Commit



# CLIENT = Github(Configuration.GITHUB_ACCESS_TOKEN)

def connect():
    '''
    
    '''
    return Github(Configuration.GITHUB_ACCESS_TOKEN)


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
    client = connect()
    user = User.create_from_api(client.get_user())
    return user.serialize







@app.route('/repo/last/modified', methods=['GET'])
def repo_last_modified():
    '''
    
    '''
    client = connect()
    user = client.get_user()
    print(client)
    print(user)
    print(user.name)
    user = User.create_from_api(client.get_user())
    return jsonify(user.serialize)


