from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Rambo123@localhost/TestShop'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view= 'login_page' 
login_manager.login_message_category = 'info' 
oauth = OAuth(app)

from market import routes
