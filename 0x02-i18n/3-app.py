#!/usr/bin/env python3
"""
Flask app module
"""
from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)


class config:
    """ Settings for Babel configurations"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(config)

babel = Babel(app)

@babel.localeselector
def get_locale():
    """ determines best match for supported Lang'"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """ The index route"""
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)