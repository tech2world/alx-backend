#!/usr/bin/env python3
"""
Use user locale
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from config import Config

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
    user_id = request.args.get('login_as')
    if user_id and int(user_id) in users:
        return users[int(user_id)]
    return None


@app.before_request
def before_request():
    g.user = get_user()


@babel.localeselector
def get_locale():
    if 'locale' in request.args and request.args['locale'] in app.config['LANGUAGES']:
        return request.args['locale']
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
