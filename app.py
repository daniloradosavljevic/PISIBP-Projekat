from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
 
app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'baze'
 
mysql = MySQL(app)

@app.route('/')
def home():
    ulogovan = False
    if "loggedin" in session and session["loggedin"]:
        ulogovan = True
        return render_template("index.html", ulogovan=ulogovan)
    else:
        return render_template("index.html", ulogovan=ulogovan)


@app.route("/cms/login", methods=["GET", "POST"])
def login():
    if "loggedin" in session and session["loggedin"]:
        return redirect(url_for("home"))

    msg = ""

    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))

        account = cursor.fetchone()

        if account and bcrypt.check_password_hash(account["password"], password):
            session["loggedin"] = True
            session["id"] = account["id"]
            session["username"] = account["username"]
            session["uloga"] = account["uloga"]
            msg = "Logged in successfully!"
            return redirect(url_for("home"))
        else:
            msg = "Incorrect username/password"

    return render_template("login.html", msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/cms/register", methods=["GET", "POST"])
def register():
    if "loggedin" in session and session["loggedin"] and session['uloga'] != 1:
        return redirect(url_for("home"))
    reg = False
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
        and "ime" in request.form
        and "prezime" in request.form
        and "uloga" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        password_hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        email = request.form["email"]
        ime = request.form["ime"]
        prezime = request.form["prezime"]
        uloga = request.form["uloga"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        account = cursor.fetchone()
        if account:
            msg = "Već postoji nalog sa tim username-om!"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Email adresa nije tačna"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Korisničko ime sme da ima samo slova i brojeve!"
        elif (
            not username
            or not password
            or not email
            or not ime
            or not prezime
            or not uloga
        ):
            msg = "Popunite sva polja! "
        else:
            cursor.execute(
                "INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s)",
                (
                    username,
                    ime,
                    prezime,
                    email,
                    uloga,
                    password_hashed
                ),
            )
            mysql.connection.commit()
            msg = "Uspešno ste dodali korisnika" 
            reg = True
    elif request.method == "POST":
        msg = "Popunite sva polja!"
    return render_template("register.html", msg=msg, reg=reg)
    
@app.route('/cms/zaposleni')
def zaposleni():
    if "loggedin" not in session or not session["loggedin"] or session['uloga'] != 1:
        return redirect(url_for("home"))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, username, ime, prezime, email, uloga FROM accounts")
    zaposleni = cursor.fetchall()

    uloge = {
        1: "Glavni urednik",
        2: "Urednik",
        3: "Novinar"
    }

    return render_template("zaposleni.html", zaposleni=zaposleni, uloge=uloge)

@app.route('/cms/izmeni_zaposlenog/<int:zaposleni_id>', methods=['GET', 'POST'])
def izmeni_zaposlenog(zaposleni_id):
    if "loggedin" not in session or not session["loggedin"] or session['uloga'] != 1:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM accounts WHERE id = %s", (zaposleni_id,))
    zaposlen = cursor.fetchone()

    if request.method == 'POST':
        nov_username = request.form['username']
        nov_email = request.form['email']
        novo_ime = request.form['ime']
        novo_prezime = request.form['prezime']
        nova_uloga = request.form['uloga']

        cursor.execute(
            "UPDATE accounts SET username=%s, email=%s, ime=%s, prezime=%s, uloga=%s WHERE id=%s",
            (nov_username, nov_email, novo_ime, novo_prezime, nova_uloga, zaposleni_id)
        )
        mysql.connection.commit()
        return redirect(url_for('zaposleni'))

    return render_template("izmeni_zaposlenog.html", zaposlen=zaposlen)

@app.route('/cms/ukloni_zaposlenog/<int:zaposleni_id>')
def ukloni_zaposlenog(zaposleni_id):
    if "loggedin" not in session or not session["loggedin"] or session['uloga'] != 1:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM accounts WHERE id = %s  AND uloga != 1", (zaposleni_id,))
    mysql.connection.commit()

    return redirect(url_for('zaposleni'))

@app.route('/cms')
def cms():
    if "loggedin" not in session or not session["loggedin"] :
        return redirect(url_for("home"))
    return render_template('cms.html')

if __name__ == "__main__":
    app.run(debug=True)