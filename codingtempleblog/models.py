'''
Models.py is where you will create our database "tables" AKA models.
Which are python Objects that will be mapped to tables when a migration happens.

- Migration: Taking an Object in python (AKA class) relating that object to SQL code that is from our python code.
'''

from flask_sqlalchemy import SQLAlchemy
from codingtempleblog import app,db 
from werkzeug.security import generate_password_hash, check_password_hash

# Import datetime
from datetime import datetime

# User Auth Flow mixin
from flask_login import UserMixin

# Import login_manager
from codingtempleblog import login

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# one - many relationship
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(256), nullable = False)
    post = db.relationship('Post', backref = 'author', lazy = True)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = self.set_passsword(password)

    def __repr__(self):
        return '{} has been created'.format(self.username)

    def set_passsword(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return "The title is {}, and the user is {}".format(self.title())