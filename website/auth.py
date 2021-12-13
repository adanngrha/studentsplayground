import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        
        return render_template("index.html", user=current_user)
    
    else:
        return render_template("login.html", user=current_user)
        


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register')
def register():
    if request.method == 'POST':
        
        return render_template("index.html", user=current_user)
    
    else:
        return render_template("register.html", user=current_user)