#!/usr/bin/env python3
"""
Get locale from request
"""
from flask import Flask, render_template, request
from flask_babel import Babel
from config import Config

app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """
    determine the best match with our supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """
    index page
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(debug=True)
