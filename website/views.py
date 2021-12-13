from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

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
    pass

@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    pass

@views.route('/forums')
def forums():
    pass

@views.route('/writing', methods=['GET', 'POST'])
def writing():
    pass

@views.route('/forum-detail', methods=['GET', 'POST'])
def forum_detail():
    pass

@views.route('/comment', methods=['GET', 'POST'])
def comment():
    pass

