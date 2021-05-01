from project import db, create_app

@click.command(name='create_database')
@with_appcontext
def create_database():
    db.create_all(app=create_app())