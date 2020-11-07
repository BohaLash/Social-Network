from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from social_network import db, bcrypt
from social_network.models import User
from social_network.users.forms import (
    RegistrationForm,
    LoginForm,
    EditForm,
    # ResetPasswordForm,
)
from social_network.users.utils import save_picture
from datetime import datetime


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.welcome"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            password=hashed_password,
            name=form.name.data,
            gender=bool(form.gender.data),
            city=form.city.data,
            born=int(form.born.data),
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.mypage"))
    return render_template("users/register.html", form=form)


@users.route("/welcome")
def welcome():
    db.create_all()
    return render_template("users/welcome.html")


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.mypage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # if user.all_fields():
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("main.mypage"))
            )
            # else:
            #     flash(
            #         f"""Before you can login into your account, you need to fill info about yourself!""",
            #         "primary",
            #     )
            #     redirect(url_for("users.welcome"))

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
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "users/account.html", title="Account", image_file=image_file, form=form
    )


# @users.route("/reset_password", methods=["GET", "POST"])
# def reset_password():
#     if current_user.is_authenticated:
#         return redirect(url_for("dash.dashboard"))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash("An email has been sent with instructions to reset your password", "info")
#         return redirect(url_for("users.login"))
#     return render_template("users/reset_request.html", title="Reset Password", form=form)


# @users.route("/reset_password/<token>", methods=["GET", "POST"])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for("dash.dashboard"))
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash(
#             "That is an invalid or expired token. Please try again to reset.", "warning"
#         )
#         return redirect(url_for("users.reset_password"))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
#             "utf-8"
#         )
#         user.password = hashed_password
#         db.session.commit()
#         flash(f"Your Password has been updated!", "success")
#         return redirect(url_for("users.login"))
#     return render_template("users/reset_token.html", title="Reset Password", form=form)
