from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Forums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questioner_or_writer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_or_title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    comment = db.relationship('Comments')
           
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    forum_id = db.Column(db.Integer, db.ForeignKey('forums.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    fullname = db.Column(db.String(255))
    password = db.Column(db.Text)
    major = db.Column(db.String(255))
    university = db.Column(db.String(255))
    bio = db.Column(db.Text)
    forums = db.relationship('Forums')
    comments = db.relationship('Comments')
