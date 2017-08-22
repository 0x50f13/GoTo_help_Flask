#Written by a really stupid programer!!!!
#Be careful...
#Bugs...Bugs...Bugs are everywhere :(

from __init__ import site, db, lm
from flask import Response, redirect, url_for, request, session, abort, render_template, flash, g
# from forms import LoginForm DEPRECATED
from models import User, question, likes
from models import answer as answer_model
from flask_login import login_user, logout_user, current_user, login_required, login_manager
import json
import config
from addons.search import Question_analyzer

global searcher
searcher=Question_analyzer()


@site.before_request
def before_request():
    g.user = current_user


@site.route('/')
def index():
    return render_template("index.html", user=current_user)


@site.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@site.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')  # DONE:Redirect to index


# handle login failed
@site.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@site.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')  # DONE:Create register template
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return 'User successfully registered'


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))



@site.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@site.route('/profile/<int:id>')
def profile_by_id(id):
    user = User.query.filter_by(id=id).first()
    return render_template("profile.html", user=user)



@site.route("/ask", methods=["GET", "POST"])
@login_required
def ask():
    if request.method == "GET":
        return render_template("ask.html")
    else:
        Q = question(request.form["name"],request.form["text"], request.form["tags"])
        searcher.add_question(Q.name,Q.text,Q.tags,Q.id,None)
        Q.likes = 0
        current_user.questions.append(Q)
        db.session.add(Q)
        db.session.commit()
        return redirect("/profile")



@site.route("/like/question/<int:id>")
@login_required
def like_q(id):
    like = likes.query.filter_by(user_id=current_user.id, question_id=id).first()
    if like is None:
        Q = question.query.filter_by(id=id).first()
        newLike = likes(current_user.id, id)
        db.session.add(newLike)
        Q.likes += 1
        db.session.commit()
        return redirect("/profile")
    else:
        return redirect("/profile")



@site.route("/unlike/question/<int:id>")
@login_required
def unlike_q(id):
    like = likes.query.filter_by(user_id=current_user.id, question_id=id).first()
    if like is not None:
        likes.query.filter_by(user_id=current_user.id, question_id=id).delete()
        Q = question.query.filter_by(id=id).first()
        Q.likes -= 1
        db.session.commit()
        return redirect("/profile")
    else:
        return redirect("/profile")



@site.route("/is_liked/question/<int:id>")
@login_required
def is_liked(id):
    like = likes.query.filter_by(user_id=current_user.id, question_id=id).first()
    return json.dumps({"id": id, "is_liked": (like is None)})



@site.route("/answer/<int:id>", methods=["GET", "POST"])
@login_required
def _answer(id):
    if request.method == "GET":
        return render_template("answer.html")
    else:
        Q = question.query.filter_by(id=id).first()
        #I said stupid!help(answer)
        A = answer_model(request.form['name'], 0, request.form['text'])
        Q.answers.append(A)
        db.session.add(A)
        db.session.commit()
        return "OK"



@site.route("/topic/<int:id>")
@login_required
def topic(id):
    return render_template("topic.html", q=question.query.filter_by(id=id).first())

@site.route("/bugs")
def bugs():
    return "They are everywhere.They wang to make your deadlines really dead.They want your program not to work.They are {{webapp.path}}.Ctf text:Here nothing intresting.Really.",418
@site.route("/search/<what>")
def search(what):
    return render_template("search.html",searcher.find(what))
@site.route("/delete/question/<int:id>")
@login_required
def delete(id):
    if question.query.filter_by(id=id).first().author!=current_user:
        abort(403)
    q=question.query.filter_by(id=id).first()
    for answer in q.answers:
        db.session.delete(answer)
    db.session.delete(q)

    db.session.commit()

    return redirect("/profile")


