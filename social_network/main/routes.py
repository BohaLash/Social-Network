from social_network.models import User, Post, Friendship
from social_network import db
from datetime import datetime
from social_network.main.forms import (
    NewPostForm
)
from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import or_


main = Blueprint("main", __name__)


@login_required
def getFriendship(f_id):
    return Friendship.query.filter(
        or_(Friendship.user1_id == current_user.id,
            Friendship.user2_id == current_user.id)
    ).filter(
        or_(Friendship.user1_id == f_id,
            Friendship.user2_id == f_id)
    ).first()


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


@main.route("/sql/create_all")
def createAll():
    db.create_all()
    return redirect(url_for("main.profile"))


@main.route("/new_post", methods=["GET", "POST"])
@login_required
def newpost():
    form = NewPostForm()
    if form.validate_on_submit():
        newPost = Post(
            text=form.text.data,
            user_id=current_user.id,
        )
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for("main.profile"))
    return render_template("main/new_post.html", form=form)


@main.route("/add_friend", methods=["POST"])
@login_required
def addFriend():
    f_id = int(request.form['friend_id'])
    f = getFriendship(f_id)
    if f is None:
        new_f = Friendship(user1_id=int(current_user.id), user2_id=int(f_id))
        db.session.add(new_f)
        db.session.commit()
    return 'success'


@ main.route("/del_friend", methods=["POST"])
@ login_required
def delFriend():
    f_id = int(request.form['friend_id'])
    f = getFriendship(f_id)
    if f:
        db.session.delete(f)
        db.session.commit()
    return 'success'
