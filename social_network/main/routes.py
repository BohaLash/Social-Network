from flask import render_template, url_for, redirect, Blueprint
from flask_login import login_required, current_user
from social_network.main.forms import (
    NewPostForm
)

from datetime import datetime

from social_network import db
from social_network.models import User, Post, Friendship

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/<user>")
@login_required
def profile(user=None):
    u = User.query.filter_by(username=user).first()
    if u is None:
        u = current_user
        friend = None
    else:
        friend = bool(Friendship.query.filter_by(
            user2_id=u.id, user1_id=current_user.id).scalar())
        print(friend)
    return render_template(
        "main/profile_page.html",
        user=u,
        posts=Post.query.filter_by(
            user_id=u.id
        ).order_by(
            Post.date_created.desc()
        ),
        f=friend
    )


@main.route("/new_post", methods=["GET", "POST"])
@login_required
def newpost():
    form = NewPostForm()
    if form.validate_on_submit():
        print(form.text.data)
        newPost = Post(
            text=form.text.data,
            user_id=current_user.id,
        )
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for("main.profile"))
    return render_template("main/new_post.html", form=form)
