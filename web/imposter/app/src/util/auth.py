from src.util.db_schema import db, User
from src.__init__ import login_manager

from flask import Flask, redirect, url_for
from flask_login import current_user, login_required

import functools
import re


def verify(data):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]{1,247}\.[A-Z|a-z]{2,7}\b'
    if 'email' not in data or re.fullmatch(regex, data['email']) == None:
        return False
    if 'username' not in data or len(data['username']) > 64:
        return False

    return True


def admin_required(view):
    @functools.wraps(view)
    @login_required
    def wrapped_view(**kwargs):
        if current_user.is_admin():
            return view(**kwargs)
        else:
            return redirect(url_for('auth.index') + '?status=error&message=Admin required')
    return wrapped_view
