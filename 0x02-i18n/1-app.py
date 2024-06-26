#!/usr/bin/env python3
"""
Basic flask app module
"""
from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)


class config:
    """
    Sets Babel configuration
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(config)

babel = Babel(app)


@app.route('/')
def index():
    """The route index"""
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=5000)