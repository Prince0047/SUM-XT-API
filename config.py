import click
from flask.cli import with_appcontext
from project import db, create_app
from .models import User

@click.command(name='create_table')
@with_appcontext
def create_database():
    db.create_all(app=create_app)