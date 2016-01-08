# project/__init__.py
from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import os
import json
import glob
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from project.config import BaseConfig
from flask.ext import admin
from flask.ext.admin.contrib.sqla import ModelView
from uuid import uuid4



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

@app.route('/change')
def change():
    task = request.args.get('task')
    task_id = request.args.get('id')
    return render_template("change.html", task=task, task_id=task_id)

@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "project/static/uploads/{}".format(upload_key)
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    task_id = form.get('task_id')
    text = form.get('textarea')
    mod = models.Change(text=text, task=task_id)
    db.session.add(mod)
    db.session.commit()
    change_id = mod.id

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        upload.save(destination)
        img = models.Image(path=destination, change=change_id)
        db.session.add(img)
        
    db.session.commit()

    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return redirect(url_for("upload_complete", uuid=upload_key))


@app.route("/files/<uuid>")
def upload_complete(uuid):
    """The location we send them to at the end of the upload."""

    # Get their files.
    root = "project/static/uploads/{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template("files.html",
        uuid=uuid,
        files=files,
    )


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))


@app.route('/data')
def data():
    con = models.Connection.query.all()
    test = models.Project.query.all()
    return render_template("data.html", test=test)

@app.route('/tasks')
def tasks():
    test = models.Sub_Project.query.all()
    return render_template("tasks.html", test=test)

# Customized admin interface
class CustomView(ModelView):
    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'

admin = admin.Admin(app, 'Example: Layout', base_template='layout.html')

# Add views
admin.add_view(CustomView(models.Project, db.session))
admin.add_view(CustomView(models.User, db.session))

