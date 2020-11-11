from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from social_network import db, bcrypt
from social_network.models import User
from social_network.users.forms import (
    RegistrationForm,
    LoginForm,
    EditForm
)
from social_network.users.utils import save_picture
from datetime import datetime


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data,
            gender=bool(int(form.gender.data)),
            city=form.city.data,
            born=int(form.born.data),
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.profile"))
    return render_template("users/register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("main.profile"))
            )
        else:
            flash(
                f"Sorry, the Login was unseccesfull. Please check your credentials and try again!",
                "primary",
            )
    return render_template("users/login.html", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.gender = bool(int(form.gender.data))
        current_user.city = form.city.data
        current_user.born = form.born.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        return redirect(url_for("main.profile"))
    form.fill()
    return render_template("users/edit.html", form=form)
