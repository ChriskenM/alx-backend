#!/usr/bin/env python3
""" flask app module
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from datetime import datetime

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

@babel.localeselector
def get_locale():
    # Find locale parameter in URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    # Find locale from user settings
    user_id = request.args.get('login_as')
    if user_id:
        user = users.get(int(user_id))
        if user and user['locale'] in app.config['LANGUAGES']:
            return user['locale']
    # Locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    # Find timezone parameter in URL parameters
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    # Find time zone from user settings
    user_id = request.args.get('login_as')
    if user_id:
        user = users.get(int(user_id))
        if user and user['timezone']:
            try:
                pytz.timezone(user['timezone'])
                return user['timezone']
            except pytz.exceptions.UnknownTimeZoneError:
                pass
    # Default to UTC
    return 'UTC'

@app.route('/')
def index():
    current_time = datetime.now(pytz.timezone(get_timezone()))
    return render_template('index.html', current_time=current_time.strftime('%b %d, %Y, %I:%M:%S %p'))
