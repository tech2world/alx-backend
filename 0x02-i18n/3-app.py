#!/usr/bin/env python3
"""
Parametrize templates
"""
from flask import Flask, render_template, request
from flask_babel import Babel, _
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
    return render_template('3-index.html', title=_('home_title'),
                           header=_('home_header'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
