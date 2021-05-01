from project import db, create_app

def create_database():
    db.create_all(app=create_app())