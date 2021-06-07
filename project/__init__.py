from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from decouple import config



# SECRET_KEY = config('SECRET_KEY')
# SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
# DATABASE_URL = config('DATABASE_URL')

# init SQLAlchemy so we can use it later in our models



app = Flask(__name__)

# Uncomment for loacl use

# app.config['SECRET_KEY'] = SECRET_KEY
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# # Heroku Database for postgesql

# app.config['DATABASE_URL'] = DATABASE_URL


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
static_folder = 'project/static/'
app.config['FOLDER'] = static_folder + 'upload'
app.config['FOLDER2'] = static_folder + 'download'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 30

db = SQLAlchemy(app)
def create_app():
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
