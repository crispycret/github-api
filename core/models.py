
from core import db
from flask_sqlalchemy import Model

from core.views import last_modified_repo

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    repos = db.relationship('Repo', backref='user', lazy=True)

    @property
    def serialize(self):
        results = {}
        results['id'] = self.id
        results['name'] = self.name
        results['email'] = self.email
        # results['repos'] = self.repos
        return results

    @staticmethod
    def create_from_api(user, save=False, commit=False):
        u = User(name=user.name, email=user.email)

        if (save):
            u.save() # Check if need to save before creating repos
            Repo.create_multi_from_api(user.get_repos(), save, False)
            if (commit): db.commit()
        return u



class Repo (db.Model):
    user_id = db.Column(db.Integer, db.ForiegnKey('user.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    html_url = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.String(128), unique=True, nullable=False)
    last_modified = db.Column(db.String(128), unique=True, nullable=False)
    commits = db.relationship('User', backref='repo', lazy=True)

    @property
    def serialize(self):
        results = {}
        results['user_id'] = self.user_id
        results['id'] = self.id
        results['name'] = self.name
        results['html_url'] = self.html_url
        results['created_at'] = self.created_at
        results['last_modified'] = self.last_modified
        # results['commits'] = Commit.serialize_many(self.commits)
        return results



    @staticmethod
    def create_from_api(repo, save=False, commit=False):
        r = Repo(
            name=repo.name, html_url=repo.html_user,
            created_at=repo.created_at, last_modified=repo.last_modified
        )
        if (save):
            r.save()
            Commit.create_multi_from_api(repo.get_commits(), save, False)
            if (commit): db.commit()
        return r


    @staticmethod
    def create_multi_from_api(repos, save=False, commit=False):
        results = [Repo.create_from_api(r, save, False) for r in repos]
        if (save and commit): db.commit()
        return results
        

    @staticmethod
    def get_by_last_commit():
        repos = Repo.query.all()




class Commit (db.Model):
    repo_id = db.Column(db.Integer, db.ForiegnKey('repo.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    created_at =  db.Column(db.String(128), unique=True, nullable=False)
    last_modified =  db.Column(db.String(128), unique=True, nullable=False)

    @property
    def serialize(self):
        results={}
        results['repo_id'] = self.repo_id
        results['id'] = self.id
        results['created_at'] = self.created_at
        results['last_modified'] = self.last_modified
        return results

    @staticmethod
    def create_from_api(repo_commit, save=False, commit=False):
        c = Commit(
            created_at=repo_commit.created_at,
            last_modified=repo_commit.last_modified
        )
        if (save):
            c.save()
            if (commit): db.commit()
        return c

    
    @staticmethod
    def create_multi_from_api(commits, save=False, commit=False):
        results = [Commit.create_from_api(c, save, False) for c in commits]
        if (save and commit): db.commit()
        return results


    @staticmethod
    def serialize_many(commits):
        return [commit.serialize for commit in commits]


    @staticmethod
    def get_last_commit():
        return Commit.query.all().order_by(Commit.last_modified).first()
            