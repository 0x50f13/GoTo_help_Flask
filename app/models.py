import flask_login
from __init__ import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(256), unique=True, index=True)
    password = db.Column('password', db.String(256))
    registered_on = db.Column('registered_on', db.DateTime)
    post=relationship("qa")

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    class post(db.Model):
        #type 0 is question
        #type 1 is answer
        __tablename__ = "qa"
        id = db.Column("id", db.Integer, primary_key=True)
        name = db.Column("name", db.String(32))
        type = db.Column("type", db.Integer)
        text = db.Column("text", db.String(2048))
        likes = db.Column("like_count", db.Integer)
        author = db.Column(db.Integer,db.ForeignKey("users.user_id"))
        def __init__(self,):


db.create_all()
db.session.commit()
