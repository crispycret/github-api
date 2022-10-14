

import json
import requests
from github import Github
from flask import jsonify, request

from config import Configuration

from core import app
from core.common import get_repo_with_lastest_commit
from core.models import Repo, Commit



# CLIENT = Github(Configuration.GITHUB_ACCESS_TOKEN)

def connect():
    '''
    
    '''
    return Github(Configuration.GITHUB_ACCESS_TOKEN)



@app.route('/test', methods=['GET'])
def test():
    print('test')
    return {'status': 200}


@app.route('/test/client/token')
def test_client_token():
    # print('\n\n\n')
    # print(Configuration.GITHUB_ACCESS_TOKEN)
    # print('\n\n\n')
    return {'token': Configuration.GITHUB_ACCESS_TOKEN}

@app.route('/test/client')
def test_client():
    print('\n\n\n')
    print(Configuration.GITHUB_ACCESS_TOKEN)
    print('\n\n\n')
    client = connect()
    return {'status': True}


@app.route('/update')
def update ():
    '''
    Main Github API View.
    Use the Github API to retrieve all user data and update the database with the results.
    All other views should simply reference the database.

    [OLD] 
        Retrieve all supported data from the Github API and store
        in a relation database for faster queries.
    '''
    client = connect()
    repos = client.get_user().get_repos()

    repos = Repo.create_multi_from_api(repos)
    return [repo.serialize for repo in repos]



@app.route('/repo/<name>')
def get_repo(name):
    print(name)
    r = Repo.query.filter_by(name=name).first()
    if r == None: return {}
    return r.serialize



@app.route('/repo/last/modified', methods=['GET'])
def repo_last_modified():
    '''
    Retrieve from the database the last modified repo.
    Before returning the results make a request 
    to update the database from the Github API (Async request).
    '''
    limit = request.args.get('limit', default=1, type=int)
    repos = Repo.get_by_last_commit(limit)
    return [r.serialize for r in repos]



def repo_by_modified():
    repos = Repo.get_by_last_modified()
