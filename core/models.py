
from core import db

class Repo (db.Model):

    pass

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





class Commit (db.Model):
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