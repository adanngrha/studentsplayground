import re
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
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
    
    return render_template("forums.html", user=current_user)


@views.route('/writing', methods=['GET', 'POST'])
@login_required
def writing():
    if request.method == "POST":
        return redirect('profile')
    
    return render_template("writing.html", user=current_user)


@views.route('/forum-detail')
@login_required
def forum_detail():
    
    
    return render_template("forum-detail.html", user=current_user)


@views.route('/comment', methods=['POST'])
@login_required
def comment():
    flash("Commented", category='success')


"""
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
"""