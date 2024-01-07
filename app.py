from flask import Flask, jsonify
from flask_login import LoginManager
from dotenv import load_dotenv, dotenv_values
from flask_jwt_extended import JWTManager
from main import main
from models import User
from auth import auth
from db import db

res = load_dotenv()

if not res:
    print("""
You may need to Populate your `.env` file.
Just rename `dotenv` to `.env` and Populate the Fields.
    """)

app = Flask(__name__)
config = dotenv_values()
app.config.from_mapping(config)

with app.app_context():
    jwt = JWTManager(app)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    db.init_app(app)
    db.create_all()

login_manager = LoginManager()
login_manager.login = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(str(user_id))
