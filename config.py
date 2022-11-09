import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__)) 


__SQLALCHEMY_DATABASE_URI__ = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'default.db')

if __SQLALCHEMY_DATABASE_URI__.startswith("postgres://"):
    __SQLALCHEMY_DATABASE_URI__ = __SQLALCHEMY_DATABASE_URI__.replace("postgres://", "postgresql://", 1)

class Configuration (object):
    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
    AUTHOR = os.environ.get("AUTHOR")

    SQLALCHEMY_DATABASE_URI = __SQLALCHEMY_DATABASE_URI__

    SQLALCHEMY_TRACK_MODIFICATIONS = True