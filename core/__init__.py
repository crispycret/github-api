
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from config import Configuration


app = Flask(__name__)

app.config.from_object(Configuration)

db = SQLAlchemy(app)

# Create the database connection, register the application, and apply migration naming conventions.
naming_convention = {
    'ix': 'ix_$(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

# Apply the naming_convention to the database
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))


migrate = Migrate(app, db, render_as_batch=True)


'''
[TODO]:
[Population] Make a module that can make requests to the Github API and save the results in a database for faster less accurate references.
[Retrival] Make a module that can accept requests (views) that pulls data from the database for faster reference although less accurate.
'''


from core import views