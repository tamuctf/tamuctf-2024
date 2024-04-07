from src.__init__ import db
from src.util.auth import admin_required

import src.util.db_schema as schema

from flask import Blueprint, render_template, get_flashed_messages, redirect, url_for
from flask_login import logout_user, login_required, current_user


pages = Blueprint('pages', __name__)


@pages.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html')


@pages.route('/login', methods=['GET'])
def login():
    if not current_user.is_anonymous:
        return redirect(url_for('pages.index') + '?status=info&message=Already logged in')
    return render_template('login.html')


@pages.route('/register', methods=['GET'])
def register():
    if not current_user.is_anonymous:
        return redirect(url_for('pages.index') + '?status=info&message=Already logged in')
    return render_template('register.html')


@pages.route('/botview/<id>', methods=['GET'])
@admin_required
def bot_view(id):
    payload = schema.Submission.get_submission(id)
    return render_template('submission.html', payload=payload)
