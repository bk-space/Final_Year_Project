from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import Tourist
from . import db

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('fname') +" "+ request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('cpassword')

        tourist = Tourist.query.filter_by(email=email).first()
        if tourist:
            flash("Looks like you already have an account, try with another mail id, or log in", 'warning')
            return render_template("sign_up.html")
        if password != confirm_password:
            flash("Passwords did not match, please try again", 'error')
            return render_template("sign_up.html")

        new_tourist = Tourist(name=name, email=email, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_tourist)
        db.session.commit()

        flash("You have successfully created an account", 'success')
        return redirect(url_for("auth.login"))

    return render_template("sign_up.html", title="Register")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        tourist = Tourist.query.filter_by(email=email).first()
        if not tourist:
            flash("You do not have an account, please create one and then log in", 'error')
            return render_template("log_in.html")
        if not check_password_hash(tourist.password, password):
            flash("Passwords did not match, please try again", 'error')
            return render_template("log_in.html")

        login_user(tourist, remember=remember)
        flash("You have successfully logged in", 'success')
        return redirect(url_for("main.index"))

    return render_template("log_in.html", title="Login")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", 'success')
    return redirect(url_for("main.index"))