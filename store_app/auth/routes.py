from store_app import app
from flask import (
    render_template, request, redirect, url_for, session,
    flash, Blueprint
)

from store_app.models import db, User
import gc
from store_app.auth.forms import RegistrationForm, LoginForm
from flask_login import (
    current_user, login_user, logout_user, login_required
)

auth = Blueprint('auth', __name__)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    gc.collect()
    return redirect(url_for('store.landing'))


@auth.route('/register/', methods=["GET", "POST"])
def register():
    error = ' '
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('store.landing'))
    try:
        if form.validate_on_submit():
            user = User(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                email=form.email.data,
                phonenumber=form.phonenumber.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            gc.collect()
            flash("Congratulations, Registration was successful", 'success')
            return redirect(url_for('auth.login'))
        return render_template('register.html', form=form, error=error, title='Register')
    except Exception as e:
        return render_template('register.html', form=form, title="Register")


@auth.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = ' '
    try:
        if current_user.is_authenticated:
            flash("you are already logged in", 'info')
            return redirect(url_for('store.landing'))
        if form.validate_on_submit():

            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'warning')
                return redirect(url_for('auth.login', form=form, title="Login to your account"))
            login_user(user)
            flash("you have been successfully logged in", 'success')
            gc.collect()

            # check if user is an admin or not and login to the appropriate place
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('store.landing'))

        return render_template('login.html', form=form, title="Login to your account")
    except Exception as e:
        flash(e)
        return render_template('login.html', form=form, error=error, title="Login to your account")