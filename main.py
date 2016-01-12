# Example of combining Flask-Security and Flask-Admin.
# by Steve Saporta
# April 15, 2014
#
# Uses Flask-Security to control access to the application, with "admin" and "end-user" roles.
# Uses Flask-Admin to provide an admin UI for the lists of users and roles.
# SQLAlchemy ORM, Flask-Mail and WTForms are used in supporting roles, as well.

from flask import Flask, render_template, request, url_for, redirect, g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask.ext.security import current_user, login_required, roles_required, roles_accepted, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils
from flask_mail import Mail, Message
from flask.ext.admin import Admin
from flask.ext.admin.contrib import sqla
from uuid import uuid4
from wtforms.fields import PasswordField
import random, string, os, json, glob, hashlib


# Initialize Flask and set some config values
app = Flask(__name__)
app.config['DEBUG']=True
# Replace this with your own secret key
app.config['SECRET_KEY'] = 'super-secret'
# The database must exist (although it's fine if it's empty) before you attempt to access any page of the app
# in your browser.
# I used a PostgreSQL database, but you could use another type of database, including an in-memory SQLite database.
# You'll need to connect as a user with sufficient privileges to create tables and read and write to them.
# Replace this with your own database connection string.
#xxxxx
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/flask_test'

# Set config values for Flask-Security.
# We're using PBKDF2 with salt.
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
# Replace this with your own salt.
app.config['SECURITY_PASSWORD_SALT'] = 'xxxxxxxxxxxxxxx'
app.config['SECURITY_REGISTERABLE'] = True

# Flask-Security optionally sends email notification to users upon registration, password reset, etc.
# It uses Flask-Mail behind the scenes.
# Set mail-related config values.
# Replace this with your own "from" address
app.config['SECURITY_EMAIL_SENDER'] = 'webcoreconsulting@gmail.com'
# Replace the next five lines with your own SMTP server settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'webcoreconsulting@gmail.com'
app.config['MAIL_PASSWORD'] = 'QA5-as3-MVU-5LW'


# Initialize Flask-Mail and SQLAlchemy
mail = Mail(app)
db = SQLAlchemy(app)

mail.init_app(app)

# Create a table to support a many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# Create a table to support a many-to-many relationship between Users and Projects
projects_users = db.Table(
    'projects_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer(), db.ForeignKey('project.id'))
)

# Create a table to support a many-to-many relationship between Users and Activities
activities_users = db.Table(
    'activities_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('activity_id', db.Integer(), db.ForeignKey('activity.id'))
)


# Role class
class Role(db.Model, RoleMixin):

    # Our Role has three fields, ID, name and description
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


# User class
class User(db.Model, UserMixin):

    # Our User has six fields: ID, email, password, active, confirmed_at and roles. The roles field represents a
    # many-to-many relationship using the roles_users table. Each user may have no role, one role, or multiple roles.
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    recovery_password = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )
    projects = db.relationship(
        'Project',
        secondary=projects_users,
        backref=db.backref('users', lazy='dynamic')
    )
    activities = db.relationship(
        'Activity',
        secondary=activities_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def __str__(self):
        return self.email


# Project class
class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name


# Activity class
class Activity(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = relationship(Project, backref='activity')

    def __str__(self):
        return self.name


# Change class
class Change(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    activity = relationship(Activity, backref='change')


# Image class
class Image(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    change_id = db.Column(db.Integer, db.ForeignKey('change.id'))
    change = relationship(Change, backref='image')


# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Executes before the first request is processed.
@app.before_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = utils.encrypt_password('test')
    if not user_datastore.get_user('test'):
        user_datastore.create_user(email='test', password=encrypted_password)
    if not user_datastore.get_user('admin'):
        user_datastore.create_user(email='admin', password=encrypted_password)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user('test', 'end-user')
    user_datastore.add_role_to_user('admin', 'admin')
    db.session.commit()

# Generates random password
def password_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

# Displays the home page.
@app.route('/')
# Users must be authenticated to view the home page, but they don't have to have any particular role.
# Flask-Security will display a login form if the user isn't already authenticated.
@login_required
def index():
    return render_template('index.html')


@app.route('/test')
#@roles_accepted('end-user', 'admin')
def test():
    return ""


@app.route('/recovery')
def recovery():
    return render_template('recovery.html')


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
            return render_template('set_new_pass.html')
        except:
            return "Ikke gyldig mail"
    else:
        db.session.close()
        return "Bruker eksisterer ikke"



@app.route('/set_new_password', methods=['POST'])
def set_new_password():
    email = request.form['email']
    pas = hashlib.sha224(request.form['pas']).hexdigest()
    new_pas = utils.encrypt_password(request.form['new_pas'])
    user = db.session.query(User).filter(User.email == email).first()
    print pas
    print user.recovery_password
    if user != None and pas == user.recovery_password and new_pas != None:
        user.password = new_pas
        user.recovery_password = None
        db.session.commit()
        return "Passord endret"
    else:
        return "feil.."




@app.route('/activities')
@roles_accepted('end-user', 'admin')
def activities():
    project = request.args.get('project')
    project_id = request.args.get('project_id')
    user_id = current_user.id
    activity_list = db.session.query(Activity).join(User.activities).filter(User.id == user_id).\
        filter(Activity.project_id == project_id).all()
    return render_template("activities.html", activity_list=activity_list, project=project)


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


# Customized User model for SQL-Admin
class UserAdmin(sqla.ModelView):

    column_searchable_list = ('email',)

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)



# Customized Role model for SQL-Admin
class RoleAdmin(sqla.ModelView):
    column_auto_select_related = True
    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')


# Customized Project model for SQL-Admin
class ProjectAdmin(sqla.ModelView):
    column_auto_select_related = True
    column_exclude_list = ('activity',)
    form_excluded_columns = ('activity',)
    # Prevent administration of Project unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')


# Initialize Flask-Admin
admin = Admin(app)

# Add Flask-Admin views
admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))
admin.add_view(ProjectAdmin(Project, db.session))


# If running locally, listen on all IP addresses, port 8080
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int('8080'),
        debug=app.config['DEBUG']
    )

