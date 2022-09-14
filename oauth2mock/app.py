import os
from flask import Flask
from .routes import create_routes_bp
from .oauth2 import config_oauth

os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'


class ConfigWrapper:
    def __init__(self, config):
        self.config = config

    @property
    def authorize_url(self):
        return self.config.get("authorize_url", '/authorize/')

    @property
    def token_url(self):
        return self.config.get("token_url", '/token/')

    @property
    def profile_url(self):
        return self.config.get("profile_url", '/profile/')

    @property
    def default_userdata(self):
        return self.config.get("default_userdata", {'username': 'username'})

    @property
    def scope(self):
        return self.config.get('scope', 'profile')


def create_app(config_data=None):
    config = ConfigWrapper(config_data)
    app = Flask(__name__)
    bp = create_routes_bp(config)
    app.register_blueprint(bp, url_prefix='/')
    config_oauth(app)
    return app
