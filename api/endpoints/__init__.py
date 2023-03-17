from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

from .users import users_blueprint

api_blueprint.register_blueprint(users_blueprint)
# from .roles import *
# from .tags import *
# from .content import *
# from .comments import *
# from .ratings import *
# from .reports import *