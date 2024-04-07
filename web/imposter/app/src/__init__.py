from src.util.db_schema import db, User

from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, emit

from os import environ
import bcrypt
import uuid


login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins='*')


@login_manager.user_loader
def load_user(uid):
    return User.query.filter_by(uid=uid).first()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'pages.login'

    with app.app_context():
        from src.blueprints import auth, pages, ws
        
        app.register_blueprint(auth.auth)
        app.register_blueprint(pages.pages)
        app.register_blueprint(ws)

        db.create_all()

        admin = User.query.filter_by(username='admin#0000').first()
        if admin != None:
            admin.password = bcrypt.hashpw(app.config['ADMIN_PASSWORD'].encode(), bcrypt.gensalt()).decode()
        else:
            admin = User(
                uid = uuid.uuid4().hex,
                email = 'admin@imposter.tamuctf.com',
                username = 'admin#0000',
                password = bcrypt.hashpw(app.config['ADMIN_PASSWORD'].encode(), bcrypt.gensalt()).decode(),
                admin = True
            )
            db.session.add(admin)
        db.session.commit()

        return app
