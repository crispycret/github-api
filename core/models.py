
from core import db
from flask_sqlalchemy import Model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    # repos = db.relationship('Repo', backref='user', lazy=True)

    @property
    def serialize(self):
        results = {}
        results['id'] = self.id
        results['name'] = self.name
        results['email'] = self.email
        # results['repos'] = self.repos
        return results

    @staticmethod
    def create_from_api(user):
        u = User(name=user.name, email=user.email)

        print(u.serialize)
        # db.session.add(u)
        # db.session.commit()

        # Repo.create_multi_from_api(u.id, user.get_repos())

        # print (u.serialize)
        return u



class Repo (db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    html_url = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.String(128), unique=True, nullable=False)
    last_modified = db.Column(db.String(128), unique=True, nullable=False)
    # commits = db.relationship('User', backref='repo', lazy=True)

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
    def create_from_api(user_id, repo):
        r = Repo(
            user_id=user_id,
            name=repo.name, html_url=repo.html_url,
            created_at=repo.created_at, last_modified=repo.last_modified
        )
        db.session.add(r)
        Commit.create_multi_from_api(r.id, repo.get_commits())
        
        print (r.serialize)
        return r


    @staticmethod
    def create_multi_from_api(user_id, repos):
        return [Repo.create_from_api(user_id, r) for r in repos]
        

    @staticmethod
    def get_by_last_commit():
        last_commit = Commit.get_last_commit()
        if (not last_commit): return None
        repo = Repo.query.filter_by(id=last_commit.repo_id)
        return repo




class Commit (db.Model):
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    created_at =  db.Column(db.String(128), unique=True, nullable=False)
    last_modified =  db.Column(db.String(128), unique=True, nullable=False)

    @property
    def serialize(self):
        results={}
        results['repo_id'] = self.repo_id
        results['id'] = self.id
        results['created_at'] = self.created_at
        return results

    @staticmethod
    def create_from_api(repo_id, commit):
        c = Commit(
            repo_id=repo_id,
            created_at=commit.commit.committer.date,
        )
        db.session.add(c)
        # print (c.serialize)
        return c

    
    @staticmethod
    def create_multi_from_api(repo_id, commits):
        return [Commit.create_from_api(repo_id, c) for c in commits]


    @staticmethod
    def serialize_many(commits):
        return [commit.serialize for commit in commits]


    @staticmethod
    def get_last_commit():
        return Commit.query.all().order_by(Commit.last_modified).first()
            