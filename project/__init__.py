from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models



app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jbichaxecimeeu:7bfb499f680a399bdab66115afcb5a13c8af4b5ea10f140ca195da4331f6bfe7@ec2-54-152-185-191.compute-1.amazonaws.com:5432/d665jk19lob8l2' # Local database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://swyfkfgdcndhdi:f7684f2e83dcb945fbc365b89001915e9464c23d609242119cfaa7c6514a5b1b@ec2-54-145-224-156.compute-1.amazonaws.com:5432/d9tiuqguqufkeq'
# Heroku Database for postgesql
# app.config['DATABASE_URL'] = 'postgresql://jbichaxecimeeu:7bfb499f680a399bdab66115afcb5a13c8af4b5ea10f140ca195da4331f6bfe7@ec2-54-152-185-191.compute-1.amazonaws.com:5432/d665jk19lob8l2'
app.config['DATABASE_URL'] = 'postgresql://swyfkfgdcndhdi:f7684f2e83dcb945fbc365b89001915e9464c23d609242119cfaa7c6514a5b1b@ec2-54-145-224-156.compute-1.amazonaws.com:5432/d9tiuqguqufkeq'
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
