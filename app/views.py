from app import site
from flask import Response, redirect, url_for, request, session, abort,render_template
from forms import LoginForm
@site.route('/')
def index():
    return render_template("index.html")
@site.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method=="GET":
        return render_template("login.html",form=form)#TODO:Add login template