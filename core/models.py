
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
    created_at = db.Column(db.String(128), unique=False, nullable=False)
    last_modified = db.Column(db.String(128), unique=False, nullable=True)

    commits = db.relationship('Commit', backref='repo', lazy=True)

    @property
    def serialize(self):
        results = {}
        results['id'] = self.id
        results['name'] = self.name
        results['author'] = self.author
        results['html_url'] = self.html_url
        results['created_at'] = self.created_at
        results['last_modified'] = self.last_modified
        results['commits'] = [c.serialize for c in self.commits]
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
            name=repo.name, author=repo.owner.login, html_url=repo.html_url,
            created_at=repo.created_at, last_modified=repo.last_modified
        )

        # Only track repos with the speicified author if an author has been set.
        if (r.author != Configuration.AUTHOR and Configuration.AUTHOR != None): return None
        results = Repo.query.filter_by(name = r.name).first()

        if (bool(results)):
            r = results
        else:
            db.session.add(r)
            db.session.commit()


        Commit.create_multi_from_api(r.id, repo.get_commits())        
        return r


    @staticmethod
    def create_multi_from_api(repos):
        """ Create, Add, and Save to the database all non forked repos."""
        repos = [r for r in repos if r.parent == None]
        results = [Repo.create_from_api(r) for r in repos]
        results = [r for r in results if r is not None]
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
    message =  db.Column(db.String(128), unique=False, nullable=False)
    created_at =  db.Column(db.String(128), unique=False, nullable=False)
    last_modified =  db.Column(db.String(128), unique=False, nullable=True)

    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'), nullable=False)

    @property
    def serialize(self):
        results={}
        results['id'] = self.id
        results['author'] = self.author
        results['message'] = self.message
        results['created_at'] = self.created_at
        results['last_modified'] = self.last_modified
        results['repo_id'] = self.repo_id
        return results

    @staticmethod
    def create_from_api(repo_id, commit):
        '''
        Create, Add, and Save all new commit if the committer is the speicifed author.
        '''
        c = Commit(
            repo_id=repo_id,
            author=commit.commit.author.name,
            message=commit.commit.message,
            created_at=commit.commit.committer.date,
        )

        # only track commits that were submitted by the specified author. If None track all commit authors/
        if (c.author != Configuration.AUTHOR and Configuration.AUTHOR != None): return None

        results = Commit.query.filter_by(repo_id=repo_id, created_at=c.created_at).first()

        # Fetech the commit from the database to get the ID if it exists. Otherwise, add and save it to the database
        if (bool(results)):
            c = results
        else:
            db.session.add(c)
            db.session.commit()

        return c

    
    @staticmethod
    def create_multi_from_api(repo_id, commits):
        """ 
        Retrieve all commits for the repo id if the commit is valid.
        A reason a commit would NOT be valid is that a author is defined and the committer is not that author. 
        """
        results = []
        for commit in commits:
            c = Commit.create_from_api(repo_id, commit)
            if (c): results.append(c)
        return results


    @staticmethod
    def serialize_many(commits):
        return [commit.serialize for commit in commits]


    @staticmethod
    def get_recent(limit=1):
        return Commit.query.order_by(Commit.created_at.desc()).limit(limit)







            