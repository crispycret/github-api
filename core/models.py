from datetime import datetime

from core import db
from flask_sqlalchemy import Model

from config import Configuration

class Repo (db.Model):
    '''
    
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    author = db.Column(db.String(128), unique=False, nullable=False)
    html_url = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)

    commits = db.relationship('Commit', backref='repo', lazy=True)

    @property
    def serialize(self):
        results = {}
        results['id'] = self.id
        results['name'] = self.name
        results['author'] = self.author
        results['html_url'] = self.html_url
        results['created_at'] = self.created_at
        results['commits'] = [c.serialize for c in self.commits]
        return results


    @staticmethod
    def get_by_last_commit(limit=1):
        """ Get the repos with the latest commits. """
        commits = Commit.get_recent(limit)
        if (commits == []): return []

        repos = [Repo.query.filter_by(id=commit.repo_id).first() 
                    for commit in commits]
        return repos





class Commit (db.Model):
    '''
    
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author =  db.Column(db.String(128), unique=False, nullable=False)
    message =  db.Column(db.Text, unique=False, nullable=False)
    created_at =  db.Column(db.DateTime(timezone=True), unique=False, nullable=False)

    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'), nullable=False)

    @property
    def serialize(self):
        results={}
        results['id'] = self.id
        results['author'] = self.author
        results['message'] = self.message
        results['created_at'] = self.created_at
        results['repo_id'] = self.repo_id
        return results


    @staticmethod
    def get_recent(limit=1):
        return Commit.query.order_by(Commit.created_at.desc()).limit(limit)







            