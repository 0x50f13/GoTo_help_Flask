from flask import Flask
import os
from flask_login import LoginManager
from flask_openid import OpenID

from flask_sqlalchemy import SQLAlchemy
from sys import argv



site = Flask(__name__)
site.config.from_object('config')
db = SQLAlchemy(site)
db.create_all()
lm = LoginManager()
lm.init_app(site)
lm.login_view = 'login'
