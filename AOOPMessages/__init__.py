from flask import Flask
from .config import config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app(config_name='development'):

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from AOOPMessages.main.main import main
    app.register_blueprint(main)

    from AOOPMessages.auth.auth import auth
    app.register_blueprint(auth)

    from AOOPMessages.messages.messages import messages
    app.register_blueprint(messages)

    from AOOPMessages.errors.errors_handler import errors
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()
        db.session.commit()

    return app
