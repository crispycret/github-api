

import json
import requests
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
    Retrieve from the database the last modified repo.
    Before returning the results make a request 
    to update the database from the Github API (Async request).
    '''
    repo = Repo.get_by_last_commit()

    # Make a request to the API from within the API to update the database
    # Make this async or figure out how to do this in a new thread (flask or subprocess.)
    requests.request('GET', '127.0.0.1/repo/update/all')

    return jsonify(repo.serialize)


@app.route('/repo/update/all', methods=['GET'])
def update_all():
    '''
    
    '''
    client = connect()
    user = client.get_user()
    print(client)
    print(user)
    print(user.name)
    user = User.create_from_api(client.get_user())
    return jsonify(user.serialize)
