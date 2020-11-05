from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from hrreferral import db
from werkzeug.security import generate_password_hash,check_password_hash
from hrreferral.models import Users, Applications
from hrreferral.users.forms import RegistrationForm, LoginForm, ReferralForm, ChangePassForm, SearchForm

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

@user.route('/apply',methods = ['GET','POST'])
@login_required
def apply():
    form = ReferralForm()

    if form.validate_on_submit():
        application = Applications(user_id=current_user.id,
                                    name=form.name.data,
                                    designation=form.designation.data,
                                    comp_name=form.comp_name.data,
                                    exp=form.exp.data)
        db.session.add(application)
        db.session.commit()
        flash("Application Submitted !")
        return redirect(url_for('user.profile'))

    return render_template('apply.html',form=form)

@user.route("/profile")
@login_required
def profile():
    user = Users.query.filter_by(username=current_user.username).first_or_404()
    applications = Applications.query.filter_by(mainuser=user).order_by(Applications.date.desc())
    return render_template('profile.html', applications=applications, user=user)

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
        user = Users.query.filter_by(username=form1.search.data).first()
        if user:
            applications = Applications.query.filter_by(mainuser=user).order_by(Applications.date.desc())
            return render_template('search.html',applications=applications,form1=form1)
    return render_template('search.html',form1=form1)