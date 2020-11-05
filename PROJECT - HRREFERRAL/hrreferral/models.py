from hrreferral import db,login_manager,app,admin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask_login import UserMixin,current_user
from flask_admin.contrib.sqla import ModelView
from flask import render_template,redirect, url_for


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(124))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Applications',backref = 'mainuser',lazy = True)
    contacts = db.relationship('Contactmsg',backref = 'mainuser',lazy = True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"{self.username}"

class Applications(db.Model):
    __tablename__ = 'applications'
    users = db.relationship(Users)


    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.ForeignKey('users.id'),nullable=False)
    name = db.Column(db.String(64),nullable=False)
    designation = db.Column(db.String(64),nullable=False)
    comp_name = db.Column(db.String(124),nullable=False)
    exp = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self,user_id,name,designation,comp_name,exp):
        self.user_id = user_id
        self.name = name
        self.designation = designation
        self.comp_name = comp_name
        self.exp = exp

    def __repr__(self):
        return f"Name : {self.name}, Designation : {self.designation}, Experience : {self.exp}"
    

class Contactmsg(db.Model):
    __tablename__ = 'contactform'
    users = db.relationship(Users)

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.ForeignKey('users.id'),nullable = False)
    email = db.Column(db.String(64),nullable = False)
    subject = db.Column(db.String(124))
    message = db.Column(db.String(1024),nullable = False)

    def __init__(self,user_id,email,subject,message):
        self.user_id = user_id
        self.email = email
        self.subject = subject
        self.message = message

    def __repr__(self):
        return f"E-mail : {self.email}, Message : {self.message}."

class MyModelView(ModelView):
    def is_accessible(self):
        return True if current_user.username == 'uxoriousghost' else False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login'))


admin.add_view(MyModelView(Users, db.session))
admin.add_view(MyModelView(Applications, db.session))
admin.add_view(MyModelView(Contactmsg, db.session))