import time
import requests
from user_agent import generate_user_agent

class InstagramLogin:
    def __init__(self, app):
        self.app = app

    def generate_enc_password(self, password):
        time_now = int(time.time())
        enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{time_now}:{password}"
        return enc_password

    def login(self, username, password):
        headers_login = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': generate_user_agent(),
            'viewport-width': '424',
            'x-asbd-id': '198387',
            'x-csrftoken': 'missing',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR1IMAIWPNnlPeUCa1Z9ZHzY6Pxeu3W04eOOFPE_XrauU1OR',
            'x-instagram-ajax': '1006773434',
            'x-requested-with': 'XMLHttpRequest',
        }

        enc_password = self.generate_enc_password(password)
        data_login = {
            'enc_password': enc_password,
            'username': username,
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}'
        }

        return requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                             headers=headers_login,
                             data=data_login)
