#!/usr/bin/env python3
"""
Flask app with Babel for internationalization and locale selection
"""
from flask import Flask, render_template, request
from flask_babel import Babel, _


app = Flask(__name__)


class config:
    """ settings for Babel configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(config)

babel = Babel(app)

@babel.localeselector
def get_locale():
    """ best match for requested LANG locale"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """ Index route"""
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)