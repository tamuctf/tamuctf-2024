from os import environ
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from flask import Flask, request, make_response, Response
from base64 import b64encode, b64decode

import sys
import json

FLAG = environ['FLAG']
PORT = int(environ['PORT'])

default_session = '{"admin": 0, "username": "guest"}'
key = get_random_bytes(AES.block_size)
app = Flask(__name__)


def encrypt(session):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(pad(session.encode('utf-8'), AES.block_size)))


def decrypt(session):
    raw = b64decode(session)
    cipher = AES.new(key, AES.MODE_CBC, raw[:AES.block_size])
    try:
        return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size).decode()
    except Exception:
        return None


@app.route('/')
def index():
    session = request.cookies.get('session')
    if session == None:
        res = Response(open(__file__).read(), mimetype='text/plain')
        res.set_cookie('session', encrypt(default_session).decode())
        return res
    elif (plain_session := decrypt(session)) == default_session:
        return Response(open(__file__).read(), mimetype='text/plain')
    else:
        if plain_session != None:
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
