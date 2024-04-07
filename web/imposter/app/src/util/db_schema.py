from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(320), nullable=False, unique=True)
    username = db.Column(db.String(69), nullable=False, unique=True) # 64 char name + # + 1234
    password = db.Column(db.String(60), nullable=False) # bcrypt hash
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def get_id(self):
        return self.uid

    def is_admin(self):
        user = self.query.filter_by(username=self.username).first()
        
        if user == None:
            raise UserNotFoundError(f'User \"{username}\" not found')

        if user.admin == True:
            return True
        return False

    @property
    def serialize(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'admin': self.admin,
        }


class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1024), nullable=False)

    def get_submission(id):
        submission = Submission.query.filter_by(id=id).first()

        if submission == None:
            return ""
        return submission.message
