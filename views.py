from flask import render_template, request, url_for, redirect, g, flash, session, Flask, jsonify
from flask.ext.security import current_user, login_required, roles_required, roles_accepted, utils
from flask_mail import Mail, Message
from uuid import uuid4
import random, string, hashlib, os, json, glob, ast
from __init__ import app, db, mail
from admin import *


# Displays the home page.
@app.route('/')
# Users must be authenticated to view the home page, but they don't have to have any particular role.
# Flask-Security will display a login form if the user isn't already authenticated.
@login_required
def index():
    return render_template('index.html')


@app.route('/test')
# @roles_accepted('end-user', 'admin')
def test():
    return utils.encrypt_password('123456')


# Generates random password
def password_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/recovery', methods=['POST'])
def recovery():
    email = request.form['email']
    session.pop('_flashes', None)
    return render_template('recovery.html', email=email)


@app.route('/recovery-password', methods=['POST'])
def recovery_password():
    email = request.form['email']
    pas = password_generator()
    enc_pas = hashlib.sha224(pas).hexdigest()
    user = db.session.query(User).filter(User.email == email).first()

    if user != None:
        user.recovery_password = enc_pas
        db.session.commit()
        msg = Message("Reset password",
                  sender="webcoreconsulting@gmail.com",
                  recipients=[email])
        msg.body = "Bruk dette passordet faar aa opprette et nytt: " + pas
        try:
            mail.send(msg)
            return render_template('set_new_pass.html', email=email)
        except:
            return render_template("error.html", error=323, message="Det har oppstatt en feil ved utsending av mail..")
    else:
        db.session.close()
        flash("Brukeren eksisterer ikke")
        return render_template("recovery.html")



@app.route('/set_new_password', methods=['POST'])
def set_new_password():
    email = request.form['email']
    pas = hashlib.sha224(request.form['pas']).hexdigest()
    new_pas = utils.encrypt_password(request.form['password'])
    user = db.session.query(User).filter(User.email == email).first()
    if pas != user.recovery_password:
        flash("Feil passord")
        return None
        #return render_template('set_new_pass.html', email=email)
    elif user != None and pas == user.recovery_password and new_pas != None:
        user.password = new_pas
        user.recovery_password = None
        db.session.commit()
        return render_template('set_new_pass.html', email=email)
    else:
        #return render_template("error.html", error=692, message="Det har oppstatt en feil..")
        return None





@app.route('/activities')
@roles_accepted('end-user', 'admin')
def activities():

    project = request.args.get('project')
    project_id = request.args.get('project_id')
    user_id = current_user.id
    activity_list = db.session.query(Activity).join(User.activities).filter(User.id == user_id).\
        filter(Activity.project_id == project_id).all()

    activity_list2 = db.session.query(Folder).filter(Folder.project_id == Project.id)\
        .filter(Folder.parent_id == None).all()

    for x in activity_list2:

        print x.name

    return render_template("activities.html", activity_list=activity_list2, project=project)


@app.route('/projects')
@roles_accepted('end-user', 'admin')
def projects():
    user_id = current_user.id
    project_list = db.session.query(Project).join(User.projects).filter(User.id == user_id).all()
    return render_template("projects.html", project_list=project_list)


@app.route('/activity')
@roles_accepted('end-user', 'admin')
def activity():
    activity = request.args.get('activity')
    activity_id = request.args.get('activity_id')
    return render_template("activity.html", activity=activity, activity_id=activity_id)


@app.route('/folder', methods=['GET', 'POST'])
@roles_accepted('end-user', 'admin')
def folder():

    try:
        struct = request.form['struct']
        p = ast.literal_eval(struct)

        if p['isActivity'] == 1:
            return render_template("folder.html", back="true")
        else:
            return render_template("folder.html", data=p, back="true")
    except:
        print 'test'
    user_id = current_user.id
    project_list = db.session.query(Project).join(User.projects).filter(User.id == user_id).all()

    folder_id_list = [id.id for id in project_list]
    folder_list = []
    for x in folder_id_list:
        folder_list.extend(db.session.query(Folder).filter(Folder.project_id == x).all())

    activity_list = []
    for x in folder_id_list:
        activity_list.extend(db.session.query(ActivityTest).filter(ActivityTest.project_id == x).all())

    class Children(object):
        def __init__(self, name=None, id=None, project_id=None, parent_id=None, isActivity=None, isFolder=None):
            self.name = name
            self.id = id
            self.project_id = project_id
            self.parent_id = parent_id
            self.isActivity = isActivity
            self.isFolder = isFolder

    children = []
    [children.append(Children(x.name, x.id, x.project_id, x.parent_id, 0, 1)) for x in folder_list]
    [children.append(Children(x.name, x.id, x.project_id, x.folder_id, 1, 0)) for x in activity_list]
    [children.append(Children(x.name, x.id, 'Root', 0, 0, 0)) for x in project_list]

    root_nodes = {x for x in children if x.project_id == 0}
    links = []
    for node in root_nodes:
        links.append(("Root", node.id))

    def get_nodes(node):
        d = {}
        if node == "Root":
            d["text"] = node
        else:
            d["text"] = node.name
            d["isActivity"] = node.isActivity
            d["isFolder"] = node.isFolder

        getchildren = get_children(node)
        if getchildren:
            d["nodes"] = [get_nodes(child) for child in getchildren]
        return d

    def get_children(node):
        if node == 'Root':
            return [x for x in children if x.project_id == node]
        elif node.parent_id == 0 and node.isActivity == 0:
            return [x for x in children if x.project_id == node.id and x.parent_id == None]
        else:
            if node.isActivity == 0:
                return [x for x in children if x.parent_id == node.id]

    tree = get_nodes("Root")
    text = "{'text': 'Root', 'nodes': [{'text': u'Prosjekt3'}, {'text': u'Prosjekt4', 'nodes': [{'text': u'mappe8'}]}]}"

    return render_template("folder.html", data=tree)


@app.route('/change')
@roles_accepted('end-user', 'admin')
def change():
    activity = request.args.get('activity')
    activity_id = request.args.get('activity_id')
    return render_template("change.html", activity=activity, activity_id=activity_id)


@app.route("/upload", methods=["POST"])
def upload():
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "static/uploads/{}".format(upload_key)
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    activity_id = form.get('activity_id')
    text = form.get('textarea')
    mod = Change(description=text, activity_id=activity_id)
    db.session.add(mod)
    db.session.commit()
    change_id = mod.id

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        upload.save(destination)
        img = Image(path=destination, change_id=change_id)
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
    root = "static/uploads/{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template("files.html", uuid=uuid, files=files)


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))