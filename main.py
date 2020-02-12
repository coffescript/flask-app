from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required
from flask_bootstrap import Bootstrap
import unittest

from app import create_app
from app.forms import LoginForm
from app.firestore_service import get_users, get_todos

app = create_app()

todo = ['Buy Coffee', 'Send request of buy', 'Give product to client']

@app.cli.command()
def test():
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(test)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello-world'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello-world', methods=['GET'])
@login_required
def hello_world():
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
    'user_ip': user_ip,
    'todo':get_todos(user_id=username),
    'username': username
    }

    users = get_users()
    for user in users:
        print(user.id)
        print(user.to_dict()['password'])
        

    return render_template('hello-world.html', **context)
