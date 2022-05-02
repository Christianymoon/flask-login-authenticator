from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
#database structure 
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route("/")
def index():

     return render_template("index.html")


@app.route("/search")
def search():
    nickname= request.args.get("nickname")

    user = Users.query.filter_by(username=nickname).first()

    if user:
        return user.username
    return "User not found"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    #si la peticion es de tipo post o envio
    if request.method == "POST":
        #ciframos la contraseña pasada en hash desde html
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        #obtenemos el usuario desde username y la password cifrada
        new_user = Users(username=request.form["username"], password=hashed_pw)
        db.session.add(new_user)#añadimos/ enviamos los elementos a la base de datos
        db.session.commit()#guardamos cambios

        return "You've registered succesfully"

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])

def login():
    #si la peticion es de tipo post
    if request.method == "POST":
        #Accessing the data in database -filter username html
        user = Users.query.filter_by(username=request.form["username"]).first()
        #si el usuario y la contraseña coinciden 
        if user and check_password_hash(user.password, request.form["password"]):
        
            return "Login succesfully"
        return "Login failed"
    return render_template("login.html")




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)