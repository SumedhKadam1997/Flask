from agriapp import db,login_manager,app,admin
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

    crops = db.relationship('Crops',backref = 'mainuser',lazy = True)
    contacts = db.relationship('Contactmsg',backref = 'mainuser',lazy = True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"{self.username}"

class Crops(db.Model):
    __tablename__ = 'crops'
    users = db.relationship(Users)

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.ForeignKey('users.id'),nullable=False)
    crop_name = db.Column(db.String(64),nullable=False)
    date_planted = db.Column(db.DateTime, default=datetime.utcnow)
    area = db.Column(db.Integer, nullable = False)

    fertilizers = db.relationship('Fertilizers', backref = 'maincrop', lazy = True)
    water_soluble_fertilizers = db.relationship('WaterSolubleFertilizers', backref = 'maincrop', lazy = True)


    def __init__(self,user_id,crop_name,date_planted,area):
        self.user_id = user_id
        self.crop_name = crop_name
        self.date_planted = date_planted
        self.area = area

    def __repr__(self):
        return f"Name : {self.crop_name}, Date Planted : {self.date_planted}, Area : {self.area}"


class Fertilizers(db.Model):
    __tablename__ = "fertilizers"
    crops = db.relationship(Crops)

    id = db.Column(db.Integer, primary_key = True)
    crop_id = db.Column(db.ForeignKey('crops.id'), nullable = False)
    date_of_apply = db.Column(db.Date)
    urea = db.Column(db.Integer)
    dap = db.Column(db.Integer)
    ammonium_sulphate = db.Column(db.Integer)
    bag_of_12X32X16 = db.Column(db.Integer)
    bag_of_10X26X26 = db.Column(db.Integer)
    mop = db.Column(db.Integer)
    micronutrients = db.Column(db.Integer)
    sulphur = db.Column(db.Integer)
    bag_of_19X19X19 = db.Column(db.Integer)
    bag_of_20X20X0X13 = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    notes = db.Column(db.Text)

    def __init__(self,crop_id,date_of_apply,urea,dap,ammonium_sulphate,bag_of_12X32X16,bag_of_10X26X26,mop,micronutrients,sulphur,bag_of_19X19X19,bag_of_20X20X0X13,cost,notes):
        self.crop_id = crop_id
        self.date_of_apply = date_of_apply
        self.urea = urea
        self.dap = dap
        self.ammonium_sulphate = ammonium_sulphate
        self.bag_of_12X32X16 = bag_of_12X32X16
        self.bag_of_10X26X26 = bag_of_10X26X26
        self.mop = mop
        self.micronutrients = micronutrients
        self.sulphur = sulphur
        self.bag_of_19X19X19 = bag_of_19X19X19
        self.bag_of_20X20X0X13 = bag_of_20X20X0X13
        self.cost = cost
        self.notes = notes


class WaterSolubleFertilizers(db.Model):
    __tablename__ = "watersolublefert"
    crops = db.relationship(Crops)

    id = db.Column(db.Integer, primary_key = True)
    crop_id = db.Column(db.ForeignKey('crops.id'), nullable = False)
    date_of_apply = db.Column(db.Date)
    bag_of_19X19X19 = db.Column(db.Integer)
    bag_of_13X40X13 = db.Column(db.Integer)
    bag_of_13X0X45 = db.Column(db.Integer)
    bag_of_0X52X34 = db.Column(db.Integer)
    bag_of_12X61X0 = db.Column(db.Integer)
    calcium_nitrate = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    def __init__(self,crop_id,date_of_apply,bag_of_19X19X19,bag_of_13X40X13,bag_of_13X0X45,bag_of_0X52X34,bag_of_12X61X0,calcium_nitrate,cost,notes):
        self.crop_id = crop_id
        self.date_of_apply = date_of_apply
        self.bag_of_19X19X19 = bag_of_19X19X19
        self.bag_of_13X40X13 = bag_of_13X40X13
        self.bag_of_13X0X45 = bag_of_13X0X45
        self.bag_of_0X52X34 = bag_of_0X52X34
        self.bag_of_12X61X0 = bag_of_12X61X0
        self.calcium_nitrate = calcium_nitrate
        self.cost = cost
        self.notes = notes



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

    def inaccessible_callback(self, **kwargs):
        return redirect(url_for('user.login'))


admin.add_view(MyModelView(Users, db.session))
admin.add_view(MyModelView(Crops, db.session))
admin.add_view(MyModelView(Contactmsg, db.session))
admin.add_view(MyModelView(Fertilizers, db.session))
admin.add_view(MyModelView(WaterSolubleFertilizers, db.session))
