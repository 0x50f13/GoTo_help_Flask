import flask_login
from __init__ import db,site
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey
from flask_migrate import Migrate

migrate=Migrate(site,db)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(256), unique=True, index=True)
    password = db.Column('password', db.String(256))
    registered_on = db.Column('registered_on', db.DateTime)
    questions=relationship("question")
    #questions=relationship("anwser")
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

class question(db.Model):
    #type 0 is question
    #type 1 is answer
    __tablename__ = "qa"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(32))
    type = db.Column("type", db.Integer)
    text = db.Column("text", db.String(2048))
    likes = db.Column("likes_count",db.Integer)
    author_id=db.Column(db.Integer,ForeignKey("users.user_id"))
    author = relationship("User",back_populates="questions")
    def __init__(self,name,type,text,likes=0):
        self.name=name
        self.type=type
        self.text=text
        self.likes=likes

class likes(db.Model):
    __tablename__="likes"
    user_id=db.Column("user_id",db.Integer)
    question_id=db.Column("question_id",db.Integer)
    __mapper_args__ = {"primary_key":(user_id, question_id)}
    def __init__(self,user_id,question_id):
        self.user_id=user_id
        self.question_id=question_id
     


db.create_all()
db.session.commit()
