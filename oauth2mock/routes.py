import json
from urllib.parse import urljoin

from flask import Blueprint, render_template, request
from authlib.integrations.flask_oauth2 import current_token
from .oauth2 import authorization, require_oauth


def create_routes_bp(config):
    bp = Blueprint('home', __name__)

    @bp.route('/', methods=['GET'])
    def index():
        return render_template('index.html',
                               authorize_url=urljoin(request.host_url, config.authorize_url),
                               token_url=urljoin(request.host_url, config.token_url),
                               profile_url=urljoin(request.host_url, config.profile_url),
                               config=config)

    @bp.route(config.authorize_url, methods=['GET', 'POST'])
    def oauth2_authorize():
        if request.method == 'GET':
            fields = {}
            for field in ['response_type', 'client_id', 'scope']:
                fields[field] = request.args.get(field)
            fields['redirect_uri'] = request.args.get('redirect_url')
            fields['user_json'] = json.dumps(config.default_userdata, indent=2)
            return render_template('authorize.html', **fields)

        user = request.form.get("user")
        return authorization.create_authorization_response(grant_user=user)

    @bp.route(config.token_url, methods=['POST'])
    def issue_token():
        return authorization.create_token_response()

    @bp.route(config.profile_url, methods=['GET'])
    @require_oauth(config.scope)
    def info():
        user = current_token.user
        return user

    return bp
