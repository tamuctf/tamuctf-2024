from src.util.db_schema import User

from selenium import webdriver
from flask import current_app
from flask.sessions import SecureCookieSessionInterface

import time


def generate_admin_cookie():
    admin = User.query.filter_by(username='admin#0000').first()
    session = {'_user_id': admin.uid}
    session_interface = SecureCookieSessionInterface()
    return session_interface.get_signing_serializer(current_app).dumps(dict(session))


def view_message(submission_id):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--disable-translate')
    chrome_options.add_argument('--metrics-recording-only')
    chrome_options.add_argument('--mute-audio')
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--safebrowsing-disable-auto-update')
    chrome_options.add_argument('--js-flags=--noexpose_wasm,--jitless')

    client = webdriver.Chrome(options=chrome_options)
    client.set_page_load_timeout(5)
    client.set_script_timeout(10)

    payload = f'http://localhost:{current_app.config["PORT"]}/botview/{submission_id}'

    client.get('http://localhost:8000/')
    client.add_cookie({'name': 'session', 'value': generate_admin_cookie()})
    client.get(payload)
    time.sleep(5)

    client.quit()
