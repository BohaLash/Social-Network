from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app
from social_network import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    image_file = db.Column(db.String(32), nullable=False,
                           default="default_profile.jpg")
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(
        db.Boolean(), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    born = db.Column(
        db.Integer)
    posts = db.relationship("Post", backref="author")
    friendship = db.relationship(
        "Friendship", foreign_keys='Friendship.user1_id', backref="friend")
    friendship = db.relationship(
        "Friendship", foreign_keys='Friendship.user2_id', backref="friend")

    # def all_fields(self):
    #     if name and gender and city and date_born:
    #         return True
    #     return False

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.name}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.text}', '{self.date_created}', by {self.user_id})"


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def __repr__(self):
        return f"FriendShip: user1_id={self.user1_id}, user2_id={self.user2_id}"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    user1_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def __repr__(self):
        return f"Message: '{self.text}' from '{self.user1_id}' to '{self.user1_id}' on '{self.date_created}')"
