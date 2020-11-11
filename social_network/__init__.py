from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from social_network.config import Config


db = SQLAlchemy()
# migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from social_network.users.routes import users
    from social_network.main.routes import main
    from social_network.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
