
from core import db
from flask_sqlalchemy import Model

class User(db.Model):
    id = db.PrimaryKey(auto_increment=True)
    name = db.String(128)
    email = db.String(128)

    @staticmethod
    def create_from_api(user):
        u = User()
        repos = Repo.create_multi_from_api(u.get_repos())
        return u


class Repo (db.Model):
    id = db.PrimaryKey(auto_increment=True)
    user_id = db.Reference(User.id)
    name = db.String(128)
    created_at = db.String(128)
    last_modified = db.String(128)

    @property
    def serialize(self):
        results = {}
        results['name'] = self.name
        results['html_url'] = self.html_url
        results['created_at'] = self.created_at
        results['last_modified'] = self.last_modified
        results['commits'] = Commit.serialize_many(self.commits)
        return results



    @staticmethod
    def create_from_api(repo):
        r = Repo()
        r.name = repo.name
        r.html_url = repo.html_url
        r.created_at = repo.created_at
        r.last_modified = repo.last_modified
        r.commits = Commit.create_multi_from_api(repo.get_commits())
        return r


    @staticmethod
    def create_multi_from_api(repos):
        return [Repo.create_from_api(r) for r in repos]
        



class Commit (db.Model):
    id = db.PrimaryKey(auto_increment=True)
    repo_id = db.Reference(User.id)
    created_at = db.String(128)
    last_modified = db.String(128)
    pass

    @property
    def serialize(self):
        results={}
        results['created_at'] = self.created_at
        results['last_modified'] = self.last_modified
        return results

    @staticmethod
    def create_from_api(commit):
        c = Commit()
        c.created_at = commit.created_at
        c.last_modified = commit.last_modified
        return c

    
    @staticmethod
    def create_multi_from_api(commits):
        results = []
        for commit in commits:
            new = Commit.create_from_api(commit)
            c.append(new)
        return results


    @staticmethod
    def serialize_many(commits):
        results = []
        for commit in commits:
            results.append(commit.serialize)
        return results