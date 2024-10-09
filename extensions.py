from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from app import app
from flask_login import LoginManager

mail=Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

