import os
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
import re
import ip_address as ip
from werkzeug.utils import secure_filename

# from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
bcrypt = Bcrypt(app)
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


app.secret_key = "your secret key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "baze"


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

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO novosti (naziv, kategorija, sadrzaj, id_autora, status) VALUES (%s, %s, %s, %s, %s)",
            (title, category, content, session["id"], 0),
        )
        mysql.connection.commit()

        return redirect(url_for("home"))

    return render_template("kreiraj_novosti.html")


UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/upload_image", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return {"error": "No file part"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"error": "No selected file"}, 400

    if file:
        filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filename)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO images (filename) VALUES (%s)", (file.filename,))
        mysql.connection.commit()

        return {"location": url_for("static", filename=f"uploads/{file.filename}")}

    return {"error": "Unexpected error"}, 500

def procesuiraj_sadrzaj_vesti(novosti):
    for vest in novosti:
        start_index = vest['sadrzaj'].find('<img')
        end_index = vest['sadrzaj'].find('>', start_index) + 1 if start_index != -1 else -1
        vest['sadrzaj'] = vest['sadrzaj'][start_index:end_index]


@app.route("/prikaz_novosti")
def prikaz_novosti():
    stranica = int(request.args.get('stranica', 1))
    rezultati_po_stranici = 4
    offset = (stranica - 1) * rezultati_po_stranici
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """
        SELECT novosti.id, novosti.naziv, novosti.kategorija, novosti.sadrzaj,
               novosti.status, accounts.username AS author_username
        FROM novosti
        INNER JOIN accounts ON novosti.id_autora = accounts.id
        ORDER BY novosti.id DESC
        LIMIT %s OFFSET %s
    """, (rezultati_po_stranici, offset))
    novosti = cursor.fetchall()
    procesuiraj_sadrzaj_vesti(novosti)

    return render_template("prikaz_novosti.html", novosti=novosti, stranica=stranica,rezultati_po_stranici=rezultati_po_stranici)

@app.route("/vest/<int:vest_id>")
def vest(vest_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """
        SELECT
            novosti.id,
            novosti.naziv,
            novosti.kategorija,
            novosti.sadrzaj,
            novosti.status,
            accounts.username AS author_username,
            komentari.id AS komentar_id,
            komentari.ime AS komentar_ime,
            komentari.komentar AS komentar_tekst
        FROM novosti
        INNER JOIN accounts ON novosti.id_autora = accounts.id
        LEFT JOIN komentari ON novosti.id = komentari.vest_id
        WHERE novosti.id = %s
        """,
        (vest_id,),
    )
    rezultat = cursor.fetchall()

    if rezultat:
        komentari = {}
        for red in rezultat:
            komentar_id = red.get("komentar_id")
            if komentar_id not in komentari:
                komentari[komentar_id] = {
                    "id": komentar_id,
                    "ime": red.get("komentar_ime"),
                    "komentar": red.get("komentar_tekst"),
                }

        vest_data = {
            "id": rezultat[0].get("id"),
            "naziv": rezultat[0].get("naziv"),
            "kategorija": rezultat[0].get("kategorija"),
            "sadrzaj": rezultat[0].get("sadrzaj"),
            "status": rezultat[0].get("status"),
            "author_username": rezultat[0].get("author_username"),
            "komentari": list(komentari.values()),
        }

        return render_template("vest.html", vest=vest_data)

    return url_for("home")


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
        msg = "Uspešno ste komentarisali ovu vest!"
        return render_template("komentarisi.html", vest_id=vest_id, msg=msg)

    return render_template("komentarisi.html", vest_id=vest_id)


@app.context_processor
def inject_functions():
    def broj_lajkova(vest_id, tip):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT COUNT(*) AS count FROM lajkovi_vesti WHERE id_vesti = %s AND tip = %s",
            (vest_id, tip),
        )
        rezultat = cursor.fetchone()
        return rezultat["count"]

    def broj_lajkova_komentara(komentar_id, tip):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT COUNT(*) AS count FROM lajkovi_komentara WHERE id_komentara = %s AND tip = %s",
            (komentar_id, tip),
        )
        rezultat = cursor.fetchone()
        return rezultat["count"]

    return dict(
        broj_lajkova=broj_lajkova, broj_lajkova_komentara=broj_lajkova_komentara
    )

    


@app.route("/lajkovanje/<int:vest_id>/<int:tip>", methods=["POST"])
def lajkovanje(vest_id, tip):
    public_ip = ip.get()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM lajkovi_vesti WHERE id_vesti = %s AND ip_adresa = %s",
        (vest_id, public_ip),
    )
    postoji_lajk_dislajk = cursor.fetchone()

    if postoji_lajk_dislajk:
        stari_tip = postoji_lajk_dislajk["tip"]

        # Brisemo ako korisnik hoce 2 puta da  lajkuje/dislajjkuje
        if stari_tip == tip:
            cursor.execute(
                "DELETE FROM lajkovi_vesti WHERE id_vesti = %s AND ip_adresa = %s",
                (vest_id, public_ip),
            )
        else:

            cursor.execute(
                "UPDATE lajkovi_vesti SET tip = %s WHERE id_vesti = %s AND ip_adresa = %s",
                (tip, vest_id, public_ip),
            )
    else:
        cursor.execute(
            "INSERT INTO lajkovi_vesti (id_vesti, ip_adresa, tip) VALUES (%s, %s, %s)",
            (vest_id, public_ip, tip),
        )

    mysql.connection.commit()

    return redirect(url_for("vest", vest_id=vest_id))


@app.route(
    "/lajkovanje_komentara/<int:komentar_id>/<int:vest_id>/<int:tip>", methods=["POST"]
)
def lajkovanje_komentara(komentar_id, vest_id, tip):
    public_ip = ip.get()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute(
        "SELECT * FROM lajkovi_komentara WHERE id_komentara = %s AND ip_adresa = %s",
        (komentar_id, public_ip),
    )
    postoji_lajk_dislajk = cursor.fetchone()

    if postoji_lajk_dislajk:
        stari_tip = postoji_lajk_dislajk["tip"]

        # Brišemo ako korisnik hoće 2 puta da lajkuje/dislajkuje
        if stari_tip == tip:
            cursor.execute(
                "DELETE FROM lajkovi_komentara WHERE id_komentara = %s AND ip_adresa = %s",
                (komentar_id, public_ip),
            )
        else:
            cursor.execute(
                "UPDATE lajkovi_komentara SET tip = %s WHERE id_komentara = %s AND ip_adresa = %s",
                (tip, komentar_id, public_ip),
            )
    else:
        cursor.execute(
            "INSERT INTO lajkovi_komentara (id_komentara, ip_adresa, tip) VALUES (%s, %s, %s)",
            (komentar_id, public_ip, tip),
        )

    mysql.connection.commit()

    return redirect(url_for("vest", vest_id=vest_id))


if __name__ == "__main__":
    app.run(debug=True)
