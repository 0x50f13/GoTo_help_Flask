from flask import Flask
import os
from flask_login import LoginManager
site = Flask(__name__)
SECRET_KEY="1234"
lm = LoginManager()
lm.init_app(site)
import app.views