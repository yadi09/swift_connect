from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp
    from .auth import auth_bp
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)

    # Login manager setup
    from .models import AdminUser
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(user_id)

    with app.app_context():
        from . import models, routes
        db.create_all()  # Ensure tables are created

    return app
