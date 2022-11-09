import json
import requests

from datetime import datetime, timezone
from github import Github
from flask import jsonify, request

from config import Configuration

from core import app, db
from core.common import get_repo_with_lastest_commit
from core.models import Repo, Commit

# CLIENT = Github(Configuration.GITHUB_ACCESS_TOKEN)

def connect():
    return Github(Configuration.GITHUB_ACCESS_TOKEN)


@app.route('/test', methods=['GET'])
def test(): return {'status': 200}



@app.route('/update')
def update ():
    '''
    Main Github API View.
    Use the Github API to retrieve all user data and update the database with the results.
    All other views should simply reference the database.

    [OLD] 
        Retrieve all supported data from the Github API and store
        in a relational database for faster queries.
    '''
    client = connect()
    repos = client.get_user().get_repos()

    results = []
    for r in repos:
        repo = Repo(
            name=r.name, author=r.owner.login, html_url=r.html_url,
            created_at=r.created_at
        )

        # Skip repos not authored by me
        if (repo.author != Configuration.AUTHOR and Configuration.AUTHOR != None): continue

        # Verify the repo does not already exist
        exists = Repo.query.filter_by(name=repo.name).first()

        # If it exists update the repo to access the repo object.        
        if (exists): repo = exists
        else: 
            # Otherwise add the repo and commit
            db.session.add(repo)
            db.session.commit()

        results.append(repo)

        for c in r.get_commits():
    
            # skip commits not authored by me
            if (c.author == None): continue
            if (c.author.login != Configuration.AUTHOR and Configuration.AUTHOR != None): continue

            commit = Commit(
                repo_id=repo.id, author=c.commit.author.name,
                message=c.commit.message, created_at=c.commit.committer.date.replace(tzinfo=timezone.utc),
            )

            exists = Commit.query.filter_by(repo_id=commit.repo_id, created_at=commit.created_at).first()
            if (exists): commit = exists
            else:
                db.session.add(commit)
                db.session.commit()
    
        # Finally save all commits added to the database

    
    return [repo.serialize for repo in results]


@app.route('/repos')
def get_repos():
    return [r.serialize for r in Repo.query.limit(50)]


@app.route('/repo/<name>')
def get_repo(name):
    r = Repo.query.filter_by(name=name).first()
    if r == None: return {}
    return r.serialize




@app.route('/repo/last-modified', methods=['GET'])
def repo_last_modified():
    '''
    Retrieve from the database the last modified repo.
    Before returning the results make a request 
    to update the database from the Github API (Async request).
    '''
    limit = request.args.get('limit', default=1, type=int)
    limit = limit if limit < 50 else 50 # Set limit on number of repos retrieved
    repos = Repo.get_by_last_commit(limit)
    return [r.serialize for r in repos]


