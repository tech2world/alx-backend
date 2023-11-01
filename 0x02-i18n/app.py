#!/usr/bin/env python3
"""
Display the current time
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _, format_datetime
from config import Config
import pytz
from datetime import datetime

app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user():
    """
    get user using id
    """
    user_id = request.args.get('login_as')
    if user_id and int(user_id) in users:
        return users[int(user_id)]
    return None


@app.before_request
def before_request():
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    get local language
    """
    if 'locale' in request.args and request.args['locale'] in app.config['LANGUAGES']:
        return request.args['locale']
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    get timezone
    """
    if 'timezone' in request.args:
        try:
            return pytz.timezone(request.args['timezone'])
        except pytz.UnknownTimeZoneError:
            pass
    if g.user and g.user['timezone']:
        try:
            return pytz.timezone(g.user['timezone'])
        except pytz.UnknownTimeZoneError:
            pass
    return pytz.timezone(app.config['BABEL_DEFAULT_TIMEZONE'])


@app.route('/')
def index():
    """
    index page
    """
    current_time = format_datetime(datetime.now(get_timezone()), format="medium")
    return render_template('index.html', current_time=current_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
