
from core import db
from flask_sqlalchemy import Model


class Repo (db.Model):
    '''
    
    '''
    name = db.Column(db.String(128), unique=True, nullable=False, primary_key=True)
    html_url = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.String(128), unique=False, nullable=False)
    last_modified = db.Column(db.String(128), unique=False, nullable=True)
    # commits = db.relationship('Commit', backref='repo', lazy=True)

    @property
    def serialize(self):
        results = {}
        results['name'] = self.name
        results['html_url'] = self.html_url
        results['created_at'] = self.created_at
        results['last_modified'] = self.last_modified
        # results['commits'] = Commit.serialize_many(self.commits)
        return results



    @staticmethod
    def create_from_api(repo):
        r = Repo(
            name=repo.name, html_url=repo.html_url,
            created_at=repo.created_at, last_modified=repo.last_modified
        )
        if (bool(Repo.query.filter_by(name = r.name).first())):
            print ("Repo {name} already exists.")
        else:
            db.session.add(r)
            db.session.commit()

        # Commit.create_multi_from_api(r.name, repo.get_commits())        
        return r


    @staticmethod
    def create_multi_from_api(repos):
        results = [Repo.create_from_api(r) for r in repos]
        return results
        

    @staticmethod
    def get_by_last_commit(count=1):
        commits = Commit.get_last_commit(count)
        if (commits == []): return []

        repos = [Repo.query.filter_by(name=commit.repo_name) 
                    for commit in commits]
        return repos






class Commit (db.Model):
    '''
    
    '''
    repo_name = db.Column(db.String(2128), db.ForeignKey('repo.name'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    created_at =  db.Column(db.String(128), unique=False, nullable=False)
    last_modified =  db.Column(db.String(128), unique=False, nullable=True)

    @property
    def serialize(self):
        results={}
        results['repo_name'] = self.repo_name
        results['id'] = self.id
        results['created_at'] = self.created_at
        return results

    @staticmethod
    def create_from_api(repo_name, commit):
        c = Commit(
            repo_name=repo_name,
            created_at=commit.commit.committer.date,
        )
        db.session.add(c)
        db.session.commit()
        return c

    
    @staticmethod
    def create_multi_from_api(repo_name, commits):
        return [Commit.create_from_api(repo_name, c) for c in commits]


    @staticmethod
    def serialize_many(commits):
        return [commit.serialize for commit in commits]


    @staticmethod
    def get_last_commit(count=1):
        return Commit.query.order_by(Commit.last_modified).limit(count)







            