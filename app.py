from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
import re
import bleach

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "your secret key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "baze"

# bleach koristimo za XSS security

_ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "class"],
    "table": ["class"],
}
_ALLOWED_TAGS = [
    "b",
    "i",
    "ul",
    "li",
    "p",
    "br",
    "hr",
    "a",
    "h1",
    "h2",
    "h3",
    "h4",
    "ol",
    "img",
    "strong",
    "code",
    "em",
    "blockquote",
    "table",
    "thead",
    "tr",
    "td",
    "tbody",
    "th",
    "s",
]

mysql = MySQL(app)


@app.route("/")
def home():
    ulogovan = False
    if "loggedin" in session and session["loggedin"]:
        ulogovan = True
        return render_template("index.html", ulogovan=ulogovan)
    else:
        return redirect(url_for("prikaz_novosti"))


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


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/cms/register", methods=["GET", "POST"])
def register():
    if "loggedin" in session and session["loggedin"] and session["uloga"] != 1:
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
                (username, ime, prezime, email, uloga, password_hashed),
            )
            mysql.connection.commit()
            msg = "Uspešno ste dodali korisnika"
            reg = True
    elif request.method == "POST":
        msg = "Popunite sva polja!"
    return render_template("register.html", msg=msg, reg=reg)


@app.route("/cms/zaposleni")
def zaposleni():
    if "loggedin" not in session or not session["loggedin"] or session["uloga"] != 1:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, username, ime, prezime, email, uloga FROM accounts")
    zaposleni = cursor.fetchall()

    uloge = {1: "Glavni urednik", 2: "Urednik", 3: "Novinar"}

    return render_template("zaposleni.html", zaposleni=zaposleni, uloge=uloge)


@app.route("/cms/izmeni_zaposlenog/<int:zaposleni_id>", methods=["GET", "POST"])
def izmeni_zaposlenog(zaposleni_id):
    if "loggedin" not in session or not session["loggedin"] or session["uloga"] != 1:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM accounts WHERE id = %s", (zaposleni_id,))
    zaposlen = cursor.fetchone()

    if request.method == "POST":
        nov_username = request.form["username"]
        nov_email = request.form["email"]
        novo_ime = request.form["ime"]
        novo_prezime = request.form["prezime"]
        nova_uloga = request.form["uloga"]

        cursor.execute(
            "UPDATE accounts SET username=%s, email=%s, ime=%s, prezime=%s, uloga=%s WHERE id=%s",
            (nov_username, nov_email, novo_ime, novo_prezime, nova_uloga, zaposleni_id),
        )
        mysql.connection.commit()
        return redirect(url_for("zaposleni"))

    return render_template("izmeni_zaposlenog.html", zaposlen=zaposlen)


@app.route("/cms/ukloni_zaposlenog/<int:zaposleni_id>")
def ukloni_zaposlenog(zaposleni_id):
    if "loggedin" not in session or not session["loggedin"] or session["uloga"] != 1:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "DELETE FROM accounts WHERE id = %s  AND uloga != 1", (zaposleni_id,)
    )
    mysql.connection.commit()

    return redirect(url_for("zaposleni"))


@app.route("/cms")
def cms():
    if "loggedin" not in session or not session["loggedin"]:
        return redirect(url_for("home"))
    return render_template("cms.html")


@app.route("/cms/kreiraj_novosti", methods=["GET", "POST"])
def kreiraj_novosti():
    if "loggedin" not in session or not session["loggedin"]:
        return redirect(url_for("home"))

    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        content = request.form["content"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "INSERT INTO novosti (naziv, kategorija, sadrzaj, id_autora, status) VALUES (%s, %s, %s, %s, %s)",
            (title, category, content, session["id"], 0),
        )
        mysql.connection.commit()

        return redirect(url_for("home"))

    return render_template("kreiraj_novosti.html")


@app.route("/prikaz_novosti")
def prikaz_novosti():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """
        SELECT novosti.id, novosti.naziv, novosti.kategorija, novosti.sadrzaj,
               novosti.status, accounts.username AS author_username
        FROM novosti
        INNER JOIN accounts ON novosti.id_autora = accounts.id
        ORDER BY novosti.id DESC
    """
    )
    novosti = cursor.fetchall()

    for vest in novosti:
        vest["sadrzaj"] = bleach.clean(
            vest["sadrzaj"],
            tags=_ALLOWED_TAGS,
            attributes=_ALLOWED_ATTRIBUTES,
        )

    return render_template("prikaz_novosti.html", novosti=novosti)

@app.route("/komentarisi/<int:vest_id>", methods=["GET", "POST"])
def komentarisi(vest_id):
    if request.method == "POST":
        ime = request.form["ime"]
        komentar = request.form["komentar"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "INSERT INTO komentari (vest_id, ime, komentar) VALUES (%s, %s, %s)",
            (vest_id, ime, komentar),
        )
        mysql.connection.commit()
        msg = 'Uspešno ste komentarisali ovu vest!'
        return render_template('komentarisi.html',vest_id=vest_id,msg=msg)

    return render_template('komentarisi.html',vest_id=vest_id)



if __name__ == "__main__":
    app.run(debug=True)
