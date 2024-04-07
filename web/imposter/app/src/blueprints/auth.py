from src.__init__ import db
from src.util.auth import verify
from src.util.db_schema import User

from flask import Blueprint, request, flash, redirect, url_for
from flask_login import logout_user, login_required, current_user, login_user

import werkzeug
import random
import bcrypt
import uuid


auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth.route('/register', methods=['POST'])
def register():
    try:
        # If authenticated, redirect index
        if not current_user.is_anonymous:
            return redirect(url_for('pages.index') + '?status=info&message=Already logged in')
    
        request.parameter_storage_class = werkzeug.datastructures.MultiDict
        data = request.form

        if verify(data) == False:
            return redirect(url_for('pages.register') + '?status=danger&message=An error occurred')

        data.add('uid', uuid.uuid4().hex)
        data['username'] += '#' + str(random.randint(0,10000)).rjust(4, '0')
    
        user = User.query.filter_by(email=data['email']).first()
        if user != None:
            return redirect(url_for('pages.register') + '?status=danger&message=Email already in use')
   
        data['password'] = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()

        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('pages.login') + '?status=success&message=Registration successful')
    except Exception:
        return redirect(url_for('pages.register') + '?status=danger&message=An error occurred')


@auth.route('/login', methods=['POST'])
def login():
    try:
        if not current_user.is_anonymous:
            return redirect(url_for('pages.index') + '?status=info&message=Already logged in')

        data = request.form

        user = User.query.filter_by(email=data['email']).first()
        if user == None or bcrypt.checkpw(data['password'].encode(), user.password.encode()) != True:
            return redirect(url_for('pages.login') + '?status=danger&message=Incorrect username or password')

        login_user(user)
        return redirect(url_for('pages.index') + '?status=success&message=User successfully authenticated')
    except Exception:
        return redirect(url_for('pages.login') + '?status=danger&message=An error occurred')


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('pages.login') + '?status=success&message=User logged out')
