from flask import Flask
from .routes.cleaning import cleaning_bp
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # register blueprints
    app.register_blueprint(cleaning_bp)

    return app
