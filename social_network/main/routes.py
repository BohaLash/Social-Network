from social_network.models import User, Post, Friendship, Message
from social_network import db
from datetime import datetime
from social_network.main.forms import (
    NewPostForm
)
from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import or_, and_


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


@main.route("/sql/create_all")
def createAll():
    db.create_all()
    return redirect(url_for("main.profile"))


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


@main.route("/search", methods=["GET", "POST"])
@main.route("/search/<key>", methods=["GET", "POST"])
@login_required
def search(key=None):
    if request.method == "POST":
        key = request.form['search']
        return redirect('/search/' + key)
    result = User.query.filter(
        User.id != current_user.id
    ).filter(
        or_(User.name.contains(key),
            User.username.contains(key))
    ).all()
    print(result)
    my_friends = User.query.filter(
        User.id != current_user.id
    ).filter(
        or_(User.id == Friendship.user1_id,
            User.id == Friendship.user2_id)
    ).filter(
        or_(Friendship.user1_id == current_user.id,
            Friendship.user2_id == current_user.id)
    ).all()
    friends = dict((
        u.id,
        bool(u in my_friends)
    ) for u in result)
    print(friends)
    return render_template("main/user_list.html", users=result, f=friends)


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


@main.route("/del_friend", methods=["POST"])
@login_required
def delFriend():
    f_id = int(request.form['friend_id'])
    f = getFriendship(f_id)
    if f:
        db.session.delete(f)
        db.session.commit()
    return 'success'


@main.route("/friends")
@login_required
def friends():
    friends = User.query.filter(
        User.id != current_user.id
    ).filter(
        or_(User.id == Friendship.user1_id,
            User.id == Friendship.user2_id)
    ).filter(
        or_(Friendship.user1_id == current_user.id,
            Friendship.user2_id == current_user.id)
    ).all()
    return render_template("main/user_list.html", users=friends, f=None)


@main.route("/chat/<username>", methods=["GET", "POST"])
@login_required
def chat(username):
    u = User.query.filter(User.username == username).first()
    print(u)
    if u is None:
        return redirect(url_for("main.profile"))
    if request.method == "POST":
        text = request.form['message']
        new_m = Message(
            text=text,
            user1_id=current_user.id,
            user2_id=u.id
        )
        db.session.add(new_m)
        db.session.commit()
    m = Message.query.filter(
        or_(
            and_(Message.user1_id == u.id, Message.user2_id == current_user.id),
            and_(Message.user2_id == u.id, Message.user1_id == current_user.id)
        )
    ).order_by(Message.date_created.desc()).all()
    print(m)
    return render_template("main/chat_page.html", user=u, messages=reversed(m), my_id=current_user.id)
