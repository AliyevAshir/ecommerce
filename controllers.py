
from app import app,mail
from flask import session, url_for
from flask_mail import Mail, Message
from models import OTP  # Make sure to import your OTP model
from datetime import datetime, timedelta
from extensions import db
import random
from app import app 
from models import * 
from extensions import db   
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify

from models import User, Product, Cart, Discount,  Category,Favorite,Contact,Review
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  
from app import app  
import re
from flask_login import login_required
from app import app,mail
from flask_mail import Mail, Message
from models import OTP 
from datetime import datetime, timedelta
import random
from extensions import db
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import requests