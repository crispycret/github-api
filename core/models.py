
from core import db
from flask_sqlalchemy import Model


class Repo (db.Model):
    '''
    
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    html_url = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.String(128), unique=False, nullable=False)
    last_modified = db.Column(db.String(128), unique=False, nullable=True)

    commits = db.relationship('Commit', backref='repo', lazy=True)

    @property
    def serialize(self):
        results = {}
        results['id'] = self.id
        results['name'] = self.name
        results['html_url'] = self.html_url
        results['created_at'] = self.created_at
        results['last_modified'] = self.last_modified
        # results['commits'] = Commit.serialize_many(self.commits)
        return results



    @staticmethod
    def create_from_api(repo):
        """ 
        Create the repo object. 
        If the repo already exists in the database, 
        retrieve the repo from the database to get the id. 
        Otherwise, save the repo to the databse. 
        Create all the repo's commits and save them to the database.
        """
        r = Repo(
            name=repo.name, html_url=repo.html_url,
            created_at=repo.created_at, last_modified=repo.last_modified
        )

        results = Repo.query.filter_by(name = r.name).first()

        if (bool(results)):
            r = results
        else:
            db.session.add(r)
            db.session.commit()

        print (f"Repo: {r.id}:")

        Commit.create_multi_from_api(r.id, repo.get_commits())        
        return r


    @staticmethod
    def create_multi_from_api(repos):
        results = [Repo.create_from_api(r) for r in repos]
        return results
        

    @staticmethod
    def get_by_last_commit(count=1):
        commits = Commit.get_last_commit(count)
        if (commits == []): return []

        repos = [Repo.query.filter_by(name=commit.repo_id) 
                    for commit in commits]
        return repos






class Commit (db.Model):
    '''
    
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at =  db.Column(db.String(128), unique=False, nullable=False)
    last_modified =  db.Column(db.String(128), unique=False, nullable=True)

    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'), nullable=False)

    @property
    def serialize(self):
        results={}
        results['id'] = self.id
        results['repo_id'] = self.repo_id
        results['created_at'] = self.created_at
        return results

    @staticmethod
    def create_from_api(repo_id, commit):
        c = Commit(
            repo_id=repo_id,
            created_at=commit.commit.committer.date,
        )

        results = Commit.query.filter_by(repo_id=repo_id, created_at=c.created_at).first()

        if (bool(results)):
            c = results
        else:
            db.session.add(c)
            db.session.commit()

        print (f"Repo: {repo_id}, Commit: {c.id}")
        
        return c

    
    @staticmethod
    def create_multi_from_api(repo_id, commits):
        return [Commit.create_from_api(repo_id, c) for c in commits]


    @staticmethod
    def serialize_many(commits):
        return [commit.serialize for commit in commits]


    @staticmethod
    def get_last_commit(count=1):
        return Commit.query.order_by(Commit.last_modified).limit(count)







            