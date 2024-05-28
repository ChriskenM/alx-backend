#!/usr/bin/env python3
"""
Flask app: internationalization and user login emulation.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _


app = Flask(__name__)

# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class config:
    """ Sets Babel configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(config)

babel = Babel(app)

def get_user(user_id):
    """Get user information from the mock user database."""
    return users.get(user_id)

@babel.localeselector
def get_locale():
    """Get the user's preferred locale."""
    # Check URL parameters for locale
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale

    # Check user settings for locale
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    # Check request header for locale
    header_locale = request.headers.get('Accept-Language')
    if header_locale:
        header_locale = header_locale.split(',')[0]
        if header_locale in app.config['LANGUAGES']:
            return header_locale

    # Default locale
    return app.config['BABEL_DEFAULT_LOCALE']

@app.before_request
def before_request():
    """Executed before all other functions to set the logged-in user."""
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None

@app.route('/')
def index():
    """The index route."""
    return render_template('6-index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)