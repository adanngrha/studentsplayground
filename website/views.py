import re
from flask import Blueprint, render_template, request, flash, jsonify
from flask.helpers import url_for
from flask_login import login_required, current_user
import sqlalchemy
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import all_
from sqlalchemy.sql.functions import user
from werkzeug.utils import redirect

from website.auth import login
from .models import Users, Forums, Comments
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def index():
    
    return render_template("index.html", user = current_user)


@views.route('/profile')
@login_required
def profile():
    user_id = current_user.id
    users = Users.query.filter_by(id=user_id).first()
    
    return render_template("profile.html", user=current_user, users=users)


@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    
    if request.method == "POST":
        user_id = current_user.id
        user = Users.query.filter_by(id=user_id).first()
        fullname = request.form.get('fullname')
        major = request.form.get('major')
        university = request.form.get('university')
        bio = request.form.get('bio')
        
        user.fullname = fullname
        user.major = major
        user.university = university
        user.bio = bio
        db.session.commit()
        
        return redirect('profile')
    
    user_id = current_user.id
    users = Users.query.filter_by(id=user_id).first()
    return render_template("edit-profile.html", user=current_user, users=users)


@views.route('/forums')
@login_required
def forums():
    # Query joining two tables
    all_forums = db.session.query(Users.id, Users.username, Forums.id, Forums.question_or_title, Forums.questioner_or_writer_id, Forums.description, Forums.content, Forums.date).\
        select_from(Users).join(Forums).all()
    for forum in all_forums:
        print(forum)
        
    return render_template("forums.html", user=current_user, forums=all_forums)


@views.route('/writing', methods=['GET', 'POST'])
@login_required
def writing():
    if request.method == "POST":
    
        user_id = current_user.id    
        title = request.form.get('title')
        description = request.form.get('short-description')
        content = request.form.get('content')
        new_forum = Forums(questioner_or_writer_id=user_id, question_or_title=title, description=description, content=content)
        db.session.add(new_forum)
        db.session.commit()  
        return redirect('forums')
    
    return render_template("writing.html", user=current_user)



@views.route('/forum-detail/<id>')
@login_required
def forum_detail(id):
    forum = Forums.query.filter_by(id=id).first()
    forum_id = forum.id
    comments = db.session.query(Users.id, Users.username, Comments.comment, Comments.forum_id, Comments.date, Forums.id).\
        select_from(Forums).join(Comments).join(Users).filter(Forums.id==forum_id).all()
    return render_template("forum-detail.html", user=current_user, forum=forum, comments=comments)


@views.route('/comment/<forumID>', methods=['POST'])
@login_required
def comment(forumID):
    comment = request.form.get('comment')
    comments = Comments(comment=comment, forum_id=forumID, commenter_id=current_user.id)
    db.session.add(comments)
    db.session.commit()
    
    return redirect(url_for('views.forum_detail', id=forumID))
