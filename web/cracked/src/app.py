from os import environ
from hashlib import sha1
from flask import Flask, request, make_response, Response
from base64 import b64encode, b64decode

import hmac
import json


KEY = environ['KEY']
FLAG = environ['FLAG']
PORT = int(environ['PORT'])

default_session = '{"admin": 0, "username": "guest"}'
app = Flask(__name__)


def sign(m):
    return b64encode(hmac.new(KEY.encode(), m.encode(), sha1).digest()).decode()


def verify(m, s):
    return hmac.compare_digest(b64decode(sign(m)), b64decode(s))


@app.route('/')
def index():
    session = request.cookies.get('session')
    sig = request.cookies.get('sig')
    if session == None or sig == None:
        res = Response(open(__file__).read(), mimetype='text/plain')
        res.set_cookie('session', b64encode(default_session.encode()).decode())
        res.set_cookie('sig', sign(default_session))
        return res
    elif (plain_session := b64decode(session).decode()) == default_session:
        return Response(open(__file__).read(), mimetype='text/plain')
    else:
        if plain_session != None and verify(plain_session, sig) == True:
            try:
                if json.loads(plain_session)['admin'] == True:
                    return FLAG
                else:
                    return 'You are not an administrator'
            except Exception:
                return 'You are not an administrator'
        else:
            return 'You are not an administrator'

if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
