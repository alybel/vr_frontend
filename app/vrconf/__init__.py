from flask import Blueprint

vrconf = Blueprint('vrconf', __name__)

from . import views