from flask import render_template, Blueprint

homepage = Blueprint("homepage", __name__)


@homepage.route("/")
@homepage.route("/home")
def home():
    return render_template("homepage/index.html")
