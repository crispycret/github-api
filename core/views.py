

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



@app.route('/', methods=['GET'])
def test():
    print('test')
    return {'status': 200}




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
    repos = Repo.create_multi_from_api(client.get_user().get_repos())
    return [repo.serialize for repo in repos]



@app.route('/repo/<name>')
def get_repo(name):
    r = Repo.query.filter_by(name=name).first()
    if r == None: return r
    return r.serialize



@app.route('/repo/last/modified', methods=['GET'])
def repo_last_modified():
    '''
    Retrieve from the database the last modified repo.
    Before returning the results make a request 
    to update the database from the Github API (Async request).
    '''
    count = request.args.get('count', default=1, type=int)
    print (count)
    print (request)
    print (request.args)
    repos = Repo.get_by_last_commit(count)

    # # Make a request to the API from within the API to update the database
    # # Make this async or figure out how to do this in a new thread (flask or subprocess.)
    # requests.request('GET', '127.0.0.1/repo/update/all')

    if (len(repos) == 1):
        return repos[0].serialize
    return jsonify([repo.serialize for repo in repos])



def repo_by_modified():
    repos = Repo.get_by_last_modified()