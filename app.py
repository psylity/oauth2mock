from oauth2mock.app import create_app

app = create_app({
    'authorize_url': '/oauth2/authorize/',
    'token_url': '/oauth2/token/',
    'profile_url': '/oauth2/profile/',
    'scope': 'profile',
    'default_userdata': {
        'id': '123',
        'username': 'test',
        'email': 'test@localhost.com',
    },
})
