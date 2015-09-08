from social.backends.oauth import BaseOAuth2
import requests

class DrChronoOAuth2(BaseOAuth2):
    """Drchrono OAuth authentication backend"""
    name = 'drchrono'
    AUTHORIZATION_URL = 'https://drchrono.com/o/authorize'
    ACCESS_TOKEN_URL = 'https://drchrono.com/o/token/'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    ID_KEY = 'username'

    def get_user_details(self, response):
        """Return user details from Drchono account"""
        return {'username': response.get('username'),
                'doctor': response.get('doctor'),
                'is_doctor': response.get('is_doctor')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://drchrono.com/api/users/current'
        head = 'Bearer ' + str(access_token)
        data = requests.get(url, headers={'Authorization': head})
        return data.json()
