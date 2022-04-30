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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    #si la peticion es de tipo post 
    if request.method == "POST":
        #ciframos la contraseña pasada en hash
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        #obtenemos el usuario a username y la password cifrada
        new_user = User(request.form["username"], password = hashed_pw)
        db.session.add(new_user)#añadimos los elementos a la base de datos
        db.session.commit()#guardamos cambios

        return "You've registered succesfully"

    return render_template("signup.html")







if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)