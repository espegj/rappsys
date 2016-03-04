from flask.ext.security import current_user
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib import sqla
from wtforms.fields import PasswordField

from __init__ import app, db
from models import *

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


# Customized Project model for SQL-Admin
class FolderAdmin(sqla.ModelView):
    column_auto_select_related = True
    column_exclude_list = ('activity',)
    form_excluded_columns = ('activity',)
    # Prevent administration of Project unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')


# Customized Project model for SQL-Admin
class ActivityAdmin(sqla.ModelView):
    column_auto_select_related = True
    column_exclude_list = ('activity',)
    form_excluded_columns = ('activity',)
    # Prevent administration of Project unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/admin.html')


class Changes(BaseView):
    @expose('/')
    def index(self):
        list = db.session.query(ActivityTest).all()
        return self.render('admin/changes.html', data=list)

# Initialize Flask-Admin
admin = Admin(app, base_template='layout.html', template_mode='bootstrap3')

# Add Flask-Admin views
admin.add_view(Changes(name='Endringer'))
admin.add_view(MyView(name='Administrator'))

admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))
admin.add_view(ProjectAdmin(Project, db.session))
admin.add_view(FolderAdmin(Folder, db.session))
admin.add_view(ActivityAdmin(ActivityTest, db.session))




