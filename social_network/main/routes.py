from flask import render_template, url_for, redirect, Blueprint
from flask_login import login_required, current_user
from social_network.main.forms import (
    NewPostForm
)

from datetime import datetime

from social_network import db
from social_network.models import User, Post

main = Blueprint("main", __name__)


@main.route("/mypage")
@login_required
def mypage():
    # p = Post(text='lorem hello hi !', date_created=datetime(
    #     2015, 6, 5, 8, 10, 10, 10), user_id=2)
    # db.session.add(p)
    # db.session.commit()
    return render_template("main/my_page.html", user=User.query.get(current_user.id), posts=Post.query.filter_by(user_id=current_user.id).order_by(Post.date_created.desc()))


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
        return redirect(url_for("main.mypage"))
    return render_template("main/new_post.html", form=form)
