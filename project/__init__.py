# project/__init__.py
from flask import Flask, request, jsonify, session, render_template
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from project.config import BaseConfig
from flask.ext import admin
from flask.ext.admin.contrib.sqla import ModelView



# config

app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project import models



# routes
@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.json
    user = models.User(
        email=json_data['email'],
        password=json_data['password']
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    user = models.User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'result': status})


@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})

@app.route('/data')
def data():
    con = models.Connection.query.all()
    test = models.Project.query.all()
    return render_template("data.html", test=test)

# Customized admin interface
class CustomView(ModelView):
    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'

admin = admin.Admin(app, 'Example: Layout', base_template='layout.html')

# Add views
admin.add_view(CustomView(models.Project, db.session))
admin.add_view(CustomView(models.User, db.session))

