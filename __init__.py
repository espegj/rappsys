from flask import Flask
from config import BaseConfig
from flask_mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy

# Initialize Flask and set some config values
app = Flask(__name__)
app.config.from_object(BaseConfig)

mail = Mail(app)
db = SQLAlchemy(app)
mail.init_app(app)
import views