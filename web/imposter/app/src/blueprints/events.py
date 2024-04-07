from src import socketio, db
from src.util.db_schema import Submission
from src.util.bot import view_message

from flask_socketio import emit, join_room
from flask_login import current_user, login_required
from flask import current_app
from time import sleep


@socketio.on('join')
@login_required
def handle_join():
    join_room(current_user.username)


@socketio.on('json')
@login_required
def handle_message(json):
    if json['message'] != '':
        text = json['message']
        time = json['time']
        dst = json['to']
        src = current_user.username

        message_content = f"""
            <div class="message">
                <span class="sender">{src}</span>
                <span class="timestamp">{time}</span>
                <p>{text}</p>
            </div>
        """

        emit('message', {'to': dst, 'from': src, 'content': message_content}, room=dst)
        if dst != src:
            sleep(0.5)
            emit('message', {'to': src, 'from': src, 'content': message_content}, room=src)

        if dst == 'admin#0000' and '<' in text:
            submission = Submission(message=text)
            db.session.add(submission)
            db.session.commit()
            view_message(submission.id)


@socketio.on('flag')
@login_required
def flag_command():
    msg = 'Only admin#0000 can view the flag.'
    if current_user.username == "admin#0000":
        msg = current_app.config['FLAG']

    message_content = f"""
        <div class="message">
            <span class="sender">System</span>
            <p>{msg}</p>
        </div>
    """

    emit('message', {'to': current_user.username, 'from': current_user.username, 'content': message_content}, room=current_user.username)
