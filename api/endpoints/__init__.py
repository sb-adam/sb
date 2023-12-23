from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

from .users import users_blueprint

api_blueprint.register_blueprint(users_blueprint)
# from .roles import *
# from .tags import *
from .content import content_blueprint
api_blueprint.register_blueprint(content_blueprint)
from .comments import comment_blueprint
api_blueprint.register_blueprint(comment_blueprint)
# from .ratings import *
# from .reports import *