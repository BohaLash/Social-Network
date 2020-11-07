import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "veryveryverysecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///network.db"
