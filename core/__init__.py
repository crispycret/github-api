
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Configuration


app = Flask(__name__)

app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db, render_as_batch=True)


'''
[TODO]:
[Population] Make a module that can make requests to the Github API and save the results in a database for faster less accurate references.
[Retrival] Make a module that can accept requests (views) that pulls data from the database for faster reference although less accurate.
'''


from core import views