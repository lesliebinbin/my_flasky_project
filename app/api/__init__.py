from flask import Blueprint
api = Blueprint(name='api', import_name=__name__)
from . import authentication, posts, users, comments, errors