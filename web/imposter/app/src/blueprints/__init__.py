from flask import Blueprint

ws = Blueprint('ws', __name__)

from . import events
