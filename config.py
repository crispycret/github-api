import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__)) 


class Configuration (object):
    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
    AUTHOR = os.environ.get("AUTHOR")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'default.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = True