from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from agriapp import db
import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from agriapp.models import Users, Crops, Fertilizers, WaterSolubleFertilizers
from agriapp.users.forms import RegistrationForm, LoginForm, FertilizerForm, WaterSolubleFertForm, CropForm, ChangePassForm, SearchForm

user = Blueprint('user',__name__)


@user.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Users(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thank You for Registering")
        return redirect(url_for('user.login'))

    return render_template('register.html',form = form)

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@user.route('/login',methods = ['GET','POST'])
def login():
    logout_user()
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Logged in Successfully !!")

            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html',form = form)

@user.route('/add_crop',methods = ('GET','POST'))
@login_required
def add_crop():
    form = CropForm()
    
    if form.validate_on_submit():
        crop = Crops(user_id=current_user.id, 
                    crop_name=form.crop_name.data, 
                    date_planted=form.date_planted.data, 
                    area=form.area.data)
        db.session.add(crop)
        db.session.commit()
        return redirect(url_for('user.profile'))

    return render_template('add_crop.html', form = form)

@user.route('/add_fert/<crop_id>',methods = ['GET','POST'])
@login_required
def add_fert(crop_id):
    form = FertilizerForm()
    if form.validate_on_submit():
        fertilizer = Fertilizers(crop_id=crop_id,
                                    date_of_apply=form.date_of_apply.data,
                                    urea=form.urea.data,
                                    dap=form.dap.data,
                                    ammonium_sulphate=form.ammonium_sulphate.data,
                                    bag_of_12X32X16=form.bag_of_12X32X16.data,
                                    bag_of_10X26X26=form.bag_of_10X26X26.data,
                                    mop=form.mop.data,
                                    micronutrients=form.micronutrients.data,
                                    sulphur=form.sulphur.data,
                                    bag_of_19X19X19=form.bag_of_19X19X19.data,
                                    bag_of_20X20X0X13=form.bag_of_20X20X0X13.data,
                                    cost=form.cost.data,
                                    notes=form.notes.data)
        db.session.add(fertilizer)
        db.session.commit()
        crop = Crops.query.filter_by(id=crop_id).first()
        return redirect(url_for('user.view_crop',viewcrop=crop.crop_name))
    return render_template('add_fert.html', form = form)

@user.route('/add_water_fert/<crop_id>',methods = ['GET','POST'])
@login_required
def add_water_fert(crop_id):
    form2 = WaterSolubleFertForm()
    id_crop = crop_id
    if form2.validate_on_submit():
        water_soluble_fertilizer = WaterSolubleFertilizers(crop_id=id_crop,
                                    date_of_apply=form2.date_of_apply.data,
                                    bag_of_19X19X19=form2.bag_of_19X19X19.data,
                                    bag_of_13X40X13=form2.bag_of_13X40X13.data,
                                    bag_of_13X0X45=form2.bag_of_13X0X45.data,
                                    bag_of_0X52X34=form2.bag_of_0X52X34.data,
                                    bag_of_12X61X0=form2.bag_of_12X61X0.data,
                                    calcium_nitrate=form2.calcium_nitrate.data,
                                    cost=form2.cost.data,
                                    notes=form2.notes.data)
        db.session.add(water_soluble_fertilizer)
        db.session.commit()
        crop = Crops.query.filter_by(id=id_crop).first()
        return redirect(url_for('user.view_crop',viewcrop=crop.crop_name))
    return render_template('add_water_fert.html', form2 = form2)


@user.route("/<viewcrop>")
def view_crop(viewcrop = "Banana"):
    if(current_user.is_authenticated):  
        user = Users.query.filter_by(username=current_user.username).first_or_404()
        crop = Crops.query.filter_by(crop_name=viewcrop).first()
        fertilizer = Fertilizers.query.filter_by(crop_id=crop.id).order_by(Fertilizers.date_of_apply.desc())
        water_soluble_fertilizer = WaterSolubleFertilizers.query.filter_by(crop_id=crop.id).order_by(WaterSolubleFertilizers.date_of_apply.desc())
        return render_template('view_crop.html',crop=crop, fertilizer=fertilizer, water_soluble_fertilizer=water_soluble_fertilizer, user=user)
    else:
        crop = Crops.query.filter_by(crop_name=viewcrop).first()
        fertilizer = Fertilizers.query.filter_by(crop_id=crop.id).order_by(Fertilizers.date_of_apply.desc())
        water_soluble_fertilizer = WaterSolubleFertilizers.query.filter_by(crop_id=crop.id).order_by(WaterSolubleFertilizers.date_of_apply.desc())
        return render_template('view_crop.html',crop=crop, fertilizer=fertilizer, water_soluble_fertilizer=water_soluble_fertilizer)


@user.route("/delete/<delcrop>")
@login_required
def del_crop(delcrop):
    user = Users.query.filter_by(username=current_user.username).first_or_404()
    crop = Crops.query.filter_by(crop_name=delcrop).first()

    db.session.delete(crop)
    db.session.commit()

    return redirect(url_for('user.profile'))

@user.route("/deletecrop")
@login_required
def deletecrop():
    user = Users.query.filter_by(username=current_user.username).first_or_404()
    crops = Crops.query.filter_by(user_id=user.id)

    return render_template("deletecrop.html", user = user, crops = crops)



@user.route("/profile")
@login_required
def profile():
    user = Users.query.filter_by(username=current_user.username).first_or_404()
    crops = Crops.query.filter_by(mainuser=user).order_by(Crops.date_planted.desc())
    return render_template('profile.html',crops=crops, user=user)

@user.route('/changepass',methods = ['GET','POST'])
@login_required
def changepass():
    form = ChangePassForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=current_user.username).first()
        if user.check_password(form.current_pass.data):
            user.password_hash = generate_password_hash(form.new_pass.data)
            db.session.commit()
            return redirect(url_for('user.profile'))

    return render_template('changepass.html',form=form)


@user.route('/search',methods = ['GET','POST'])
def search():
    form1 = SearchForm()

    if form1.validate_on_submit():
        pass
    return render_template('search.html',form1=form1)