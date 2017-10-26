from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, PasswordField, StringField, TextAreaField, validators, DateField
from passlib.hash import sha256_crypt

app = Flask(__name__)


#app.config
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "lryy520!"
app.config["MYSQL_DB"] = "MyFakeIns"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Init mysql
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

class RegForm(Form):
    gender = StringField("Gender", [validators.Length(min = 1, max = 4)])
    email = StringField("EMAIL", [validators.Length(min = 1, max = 30)])
    dob = DateField("Your date of birth (yyyy-mm-dd)")
    fname = StringField("First name", [validators.Length(min = 1, max = 30)])
    lname = StringField("Last name", [validators.Length(min=1, max=30)])
    hometwon = StringField("Hometown", [validators.Length(min = 1, max = 30)])
    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.EqualTo("confirm", message = "password do not match")
    ])
    confirm = PasswordField("confirm password")

@app.route('/register', methods = ["GET", "POST"])
def register():
    form = RegForm(request.form)
    if request.method == "POST" and form.validate():
        gender = form.gender.data
        email = form.email.data
        dob = form.dob.data
        fname = form.fname.data
        lname = form.lname.data
        hometown = form.hometwon.data
        password = form.password.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO USER(gender, email, dob, fname, lname, hometown, password) VALUES(%s, %s, %s, %s, %s, %s, %s)", (gender, email, dob, fname, lname, hometown, password))
        mysql.connection.commit()
        #cur.close()


        return redirect(url_for("home"))
    return render_template("register.html", form = form)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password_entered = request.form["password"]

        cur = mysql.connection.cursor()
        result = cur.execute('SELECT * FROM USER WHERE email = %s', [email])
        if result > 0:
            data = cur.fetchone()
            password = data["PASSWORD"]

            if password == password_entered:
                session["logged_in"] = True
                session["username"] = email
                return redirect(url_for("home"))
            else:
                error = "The password did not match !"
                return render_template("login.html", error = error)
            cur.close()
        else:
            error = "Email not found!"
            return render_template("login.html", error = error)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

#@app.route("/myabulm")
#def myabulm():
#    return



if __name__ == '__main__':
    app.secret_key = "nmsl!"
    app.run(debug=True)
