import json
from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.oauth2.rfc6749 import grants, AuthorizationCodeMixin
from authlib.oauth2.rfc7636 import CodeChallenge
from authlib.oauth2.rfc6750 import BearerTokenValidator


class MockToken:
    def __init__(self, token_data, user):
        self.token_data = token_data
        self.user = user

    def is_expired(self):
        return False

    def is_revoked(self):
        return False

    def get_scope(self):
        return self.token_data['scope']


class MockClient(object):
    def check_redirect_uri(self, url):
        return True

    def check_response_type(self, response_type):
        return True

    def check_client_secret(self, secret):
        return True

    def check_endpoint_auth_method(self, auth_method, endpoint):
        return True

    def check_grant_type(self, grant_type):
        return True

    def get_allowed_scope(self, scope):
        return scope


class OAuth2AuthorizationCode(AuthorizationCodeMixin):
    def __init__(self, code_challenge, code_challenge_method, code, request):
        super().__init__()
        self.code_challenge = code_challenge
        self.code_challenge_method = code_challenge_method
        self.code = code
        self.request = request

    def get_redirect_uri(self):
        return self.request.data.get("redirect_uri")

    def get_scope(self):
        # TODO: config
        return 'user_info'


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    auth_codes = {}

    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic',
        'client_secret_post',
        'none',
    ]

    def save_authorization_code(self, code, request):
        code_challenge = request.data.get('code_challenge')
        code_challenge_method = request.data.get('code_challenge_method')
        auth_code = OAuth2AuthorizationCode(
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            code=code,
            request=request
        )
        self.auth_codes[code] = auth_code
        return auth_code

    def query_authorization_code(self, code, client):
        if code not in self.auth_codes:
            return None

        return self.auth_codes[code]

    def authenticate_user(self, authorization_code):
        return json.loads(authorization_code.request.data.get("user"))

    def delete_authorization_code(self, authorization_code):
        if authorization_code not in self.auth_codes:
            return
        del self.auth_codes[authorization_code]


tokens = {}


def query_client(client_id):
    return MockClient()


def save_token(token, request):
    tokens[token['access_token']] = MockToken(token, request.user)


authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)

require_oauth = ResourceProtector()


class MockBearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        return tokens[token_string]

    def request_invalid(self, request):
        return False

    def token_revoked(self, token):
        return False


def config_oauth(app):
    authorization.init_app(app)
    authorization.register_grant(AuthorizationCodeGrant, [CodeChallenge(required=True)])
    require_oauth.register_token_validator(MockBearerTokenValidator())
