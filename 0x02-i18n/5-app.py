#!/usr/bin/env python3
"""
Flask app: Babel for internationalization and user login emulation.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _


app = Flask(__name__)


# Mock user's database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class config:
    """ Configs Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(config)

babel = Babel(app)

def get_user(user_id):
    """ Gets user information"""
    return users.get(user_id)

@app.before_request
def before_request():
    """ Sets logged in user"""
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None

@app.route('/')
def index():
    """The index route."""
    return render_template('5-index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
