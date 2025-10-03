from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
import redis

# cria instâncias globais
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # carrega configurações
    app.config.from_object("back.config.Config")

    # inicializa extensões
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # inicializa redis
    app.redis = redis.from_url(app.config["REDIS_URL"])

    # registra blueprints
    from back.routes import auth_bp, products_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')

    return app
