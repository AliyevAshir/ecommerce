from flask import Flask,request 

app = Flask(__name__)

from flask_mail import Mail, Message

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:12345@localhost:3306/ecommerce"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = '5307af8b5240a5366c9cf3cc3c838c7fe9893f1a9e1227609091ded7e8593f46'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USERNAME'] = 'cyberaz191@gmail.com'
app.config['MAIL_PASSWORD'] = 'gurw zate pfjn aszt'
app.config['MAIL_DEFAULT_SENDER'] = 'cyberaz191@gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from admin import *
# from flask_wtf.csrf import CSRFProtect

# csrf = CSRFProtect(app)

mail=Mail(app)

from routes import *    
from models import *


if __name__ == '__main__':
    
    
    app.run(debug=True)