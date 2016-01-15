from flask.ext.security import current_user, login_required, roles_required, roles_accepted, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils

from __init__ import app, db
from models import *

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



# If running locally, listen on all IP addresses, port 8080
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int('8080'),
        debug=app.config['DEBUG']
    )

