from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
products_bp = Blueprint('products', __name__)


from back.routes import auth, products