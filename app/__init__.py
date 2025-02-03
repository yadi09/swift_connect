from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager

jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .api.business_requests import business_requests_bp
    from .api.admin import admin_bp
    from .routes import bp
    app.register_blueprint(bp)
    app.register_blueprint(business_requests_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")

    with app.app_context():
        from . import models, routes
        db.create_all()  # Ensure tables are created
    return app
