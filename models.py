from __init__ import db, app
from sqlalchemy.orm import relationship
from flask.ext.security import RoleMixin, UserMixin, SQLAlchemyUserDatastore, Security


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
    db.Column('activity_id', db.Integer(), db.ForeignKey('activity_test.id'))
)

shortdesc_change = db.Table(
    'shortdesc_change',
    db.Column('change_id', db.Integer(), db.ForeignKey('change.id')),
    db.Column('shortdesc_id', db.Integer(), db.ForeignKey('shortdesc.id'))
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
        'ActivityTest',
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


# Folder class
class Folder(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = relationship(Project, backref='folder')

    def __str__(self):
        return self.name


# ActivityTest class
class ActivityTest(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    isActivity = db.Column(db.Integer)
    quantity = db.Column(db.String(255))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = relationship(Project, backref='ActivityTest')
    folder = relationship(Folder, backref='ActivityTest')

    def __str__(self):
        return self.name



# Change class
class Change(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    activity_test_id = db.Column(db.Integer, db.ForeignKey('activity_test.id'))
    activity_test = relationship(ActivityTest, backref='change')
    shortdescs = db.relationship(
        'Shortdesc',
        secondary=shortdesc_change,
        backref=db.backref('change', lazy='dynamic')
    )

# Unit class
class Unit(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    activity = relationship(ActivityTest, backref='Unit')

    def __str__(self):
        return self.name


class Shortdesc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name


# Image class
class Image(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    change_id = db.Column(db.Integer, db.ForeignKey('change.id'))
    change = relationship(Change, backref='image')


# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)