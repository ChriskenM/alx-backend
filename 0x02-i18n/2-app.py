#!/usr/bin/env python3
"""
simple flask app
"""
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)


class config:
    """Sets up Babel configs
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(config)

babel = Babel(app)

@babel.localeselector
def get_locale():
    """ Determines best language match"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """ Indexes routes"""
    return render_template('2-index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)