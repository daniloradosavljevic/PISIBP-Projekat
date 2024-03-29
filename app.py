import os
from flask import (
    Flask,
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
import datetime

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
        return redirect(url_for("najnovije_vesti"))
    else:
        return redirect(url_for("najnovije_vesti"))


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
    if "loggedin" not in session or not session["loggedin"] or session["uloga"] == 3:
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

    cursor = mysql.connection.cursor()
    if session["uloga"] == 1:
        cursor.execute("SELECT id, naziv FROM kategorije")
    else:
        cursor.execute(
            """
            SELECT kategorije.id, kategorije.naziv
            FROM kategorije
            JOIN novinari_kategorije ON kategorije.id = novinari_kategorije.kategorija_id
            WHERE novinari_kategorije.novinar_id = %s
        """,
            (session["id"],),
        )
    categories = cursor.fetchall()

    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        content = request.form["content"]
        tags = request.form["tags"]

        tags = re.sub(r"<[^>]+>", "", tags)

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO novosti (naziv, kategorija, sadrzaj, id_autora, status, datum, tagovi) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (title, category, content, session["id"], 0, date, tags),
        )
        mysql.connection.commit()

        return redirect(url_for("home"))

    return render_template("kreiraj_novosti.html", categories=categories)


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


@app.route("/cms/izmeni_novost/<int:novost_id>", methods=["GET", "POST"])
def izmeni_novost(novost_id):
    if "loggedin" not in session or not session["loggedin"]:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, naziv FROM kategorije")
    categories = cursor.fetchall()

    cursor.execute("SELECT * FROM novosti WHERE id = %s", (novost_id,))
    novost = cursor.fetchone()
    if not novost:
        return redirect(url_for("home"))

    if session["id"] != novost[4]:
        return redirect(url_for("home"))

    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        content = request.form["content"]
        tags = request.form["tags"]

        tags = re.sub(r"<[^>]+>", "", tags)

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE novosti SET naziv=%s, kategorija=%s, sadrzaj=%s, tagovi=%s WHERE id=%s",
            (title, category, content, tags, novost_id),
        )
        mysql.connection.commit()

        return redirect(url_for("pregled_novosti"))
    return render_template("izmeni_novost.html", categories=categories, novost=novost)


def procesuiraj_sadrzaj_vesti(novosti):
    for vest in novosti:
        start_index = vest["sadrzaj"].find("<img")
        end_index = (
            vest["sadrzaj"].find(">", start_index) + 1 if start_index != -1 else -1
        )
        vest["sadrzaj"] = vest["sadrzaj"][start_index:end_index]


@app.route("/prikaz_novosti")
def prikaz_novosti():
    stranica = int(request.args.get("stranica", 1))
    rezultati_po_stranici = 4
    offset = (stranica - 1) * rezultati_po_stranici

    search_query = request.args.get("search_query", "")
    category = request.args.get("category", "")

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
    SELECT novosti.id, novosti.naziv, kategorije.naziv AS kategorija, 
           novosti.sadrzaj, novosti.datum, accounts.username AS author_username
    FROM novosti
    INNER JOIN accounts ON novosti.id_autora = accounts.id
    INNER JOIN kategorije ON novosti.kategorija = kategorije.id
    WHERE 1=1 AND novosti.status = 1
    """

    params = []

    if search_query:
        query += " AND (novosti.naziv LIKE %s OR novosti.sadrzaj LIKE %s OR novosti.tagovi LIKE %s OR novosti.datum LIKE %s)"
        params.extend(
            [
                f"%{search_query}%",
                f"%{search_query}%",
                f"%{search_query}%",
                f"%{search_query}%",
            ]
        )

    if category:
        query += " AND novosti.kategorija = %s"
        params.append(category)

    query += " ORDER BY novosti.id DESC LIMIT %s OFFSET %s"
    params.extend([rezultati_po_stranici, offset])

    cursor.execute(query, params)
    novosti = cursor.fetchall()
    procesuiraj_sadrzaj_vesti(novosti)

    cursor.execute("SELECT * FROM kategorije")
    categories = cursor.fetchall()

    return render_template(
        "prikaz_novosti.html",
        novosti=novosti,
        stranica=stranica,
        rezultati_po_stranici=rezultati_po_stranici,
        categories=categories,
        search_query=search_query,
        category=category,
    )


@app.route("/vest/<int:vest_id>")
def vest(vest_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        """
    SELECT
        novosti.id,
        novosti.naziv,
        kategorije.naziv AS kategorija,
        novosti.sadrzaj,
        novosti.datum,
        novosti.tagovi, -- Fetching tags from 'novosti' table
        accounts.username AS author_username,
        komentari.id AS komentar_id,
        komentari.ime AS komentar_ime,
        komentari.komentar AS komentar_tekst
    FROM novosti
    INNER JOIN accounts ON novosti.id_autora = accounts.id
    LEFT JOIN komentari ON novosti.id = komentari.vest_id
    INNER JOIN kategorije ON novosti.kategorija = kategorije.id
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
            "datum": rezultat[0].get("datum"),
            "tagovi": rezultat[0].get("tagovi"),
            "author_username": rezultat[0].get("author_username"),
            "komentari": list(komentari.values()),
        }

        return render_template("vest.html", vest=vest_data)
    else:
        return redirect(url_for("home"))


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


@app.route("/lajkovanje/<int:vest_id>/<int:tip>", methods=["GET", "POST"])
def lajkovanje(vest_id, tip):
    public_ip = ip.get()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM novosti WHERE id = %s" % vest_id)
    postoji_vest = cursor.fetchone()

    if not postoji_vest:
        return redirect(url_for("home"))

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
    "/lajkovanje_komentara/<int:komentar_id>/<int:vest_id>/<int:tip>",
    methods=["GET", "POST"],
)
def lajkovanje_komentara(komentar_id, vest_id, tip):
    public_ip = ip.get()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM komentari WHERE id = %s" % komentar_id)
    postoji_komentar = cursor.fetchone()

    if not postoji_komentar:
        return redirect(url_for("home"))

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


@app.route("/cms/prikaz_kategorija", methods=["GET", "POST"])
def prikaz_kategorija():
    if "loggedin" not in session or not session["loggedin"] and session["uloga"] != 1:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM kategorije")
    kategorije = cursor.fetchall()

    return render_template("prikaz_kategorija.html", kategorije=kategorije)


@app.route("/cms/izmeni_kategoriju/<int:kategorija_id>", methods=["GET", "POST"])
def izmeni_kategoriju(kategorija_id):
    if "loggedin" not in session or not session["loggedin"] and session["uloga"] != 1:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()

    if request.method == "POST":
        nova_vrednost = request.form["nova_vrednost"]
        cursor.execute(
            "UPDATE kategorije SET naziv = %s WHERE id = %s",
            (nova_vrednost, kategorija_id),
        )
        mysql.connection.commit()
        return redirect(url_for("prikaz_kategorija"))

    return redirect(url_for("prikaz_kategorija"))


@app.route("/cms/obrisi_kategoriju/<int:kategorija_id>", methods=["POST"])
def obrisi_kategoriju(kategorija_id):
    if "loggedin" not in session or not session["loggedin"] and session["uloga"] != 1:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM kategorije WHERE id = %s", (kategorija_id,))
    mysql.connection.commit()

    return redirect(url_for("prikaz_kategorija"))


@app.route("/cms/obrisi_novost/<int:novost_id>", methods=["GET", "POST"])
def obrisi_novost(novost_id):
    if "loggedin" not in session or not session["loggedin"]:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_autora FROM novosti WHERE id = %s", (novost_id,))
    result = cursor.fetchone()

    cursor.execute("SELECT status FROM novosti WHERE id = %s", (novost_id,))
    status_result = cursor.fetchone()

    if not result:
        return redirect(url_for("home"))

    id_autora = result[0]

    if session["uloga"] == 1:

        cursor.execute("DELETE FROM novosti WHERE id = %s", (novost_id,))
        mysql.connection.commit()

        return redirect(url_for("pregled_novosti"))

    elif session["uloga"] == 2:
        cursor.execute(
            "SELECT kategorija FROM novosti WHERE id = %s",
            (novost_id,),
        )
        kategorija_vesti = cursor.fetchone()
        cursor.execute(
            "SELECT kategorija_id FROM novinari_kategorije WHERE novinar_id = %s",
            (session["id"],),
        )
        id_list = [row[0] for row in cursor.fetchall()]
        if int(kategorija_vesti[0]) in id_list:
            cursor.execute(
                "DELETE FROM novosti WHERE id = %s",
                (novost_id,),
            )
            mysql.connection.commit()

            return redirect(url_for("pregled_novosti"))
        else:
            return redirect(url_for("pregled_novosti"))

    elif session["uloga"] == 3 and (
        session["id"] == id_autora and status_result[0] == 0
    ):
        cursor.execute(
            "DELETE FROM novosti WHERE id = %s",
            (novost_id,),
        )
        mysql.connection.commit()
        return redirect(url_for("home"))

    return redirect(url_for("pregled_novosti"))


@app.route("/cms/dodaj_kategoriju", methods=["GET", "POST"])
def dodaj_kategoriju():
    if "loggedin" not in session or not session["loggedin"] and session["uloga"] != 1:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()

    if request.method == "POST":
        nova_vrednost = request.form.get("nova_vrednost")

        if nova_vrednost:
            cursor.execute(
                "INSERT INTO kategorije (naziv) VALUES (%s)", (nova_vrednost,)
            )
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("prikaz_kategorija"))
        else:
            return redirect(url_for("prikaz_kategorija"))

    return render_template("dodaj_kategoriju.html")


@app.route("/cms/pregled_novosti")
def pregled_novosti():
    if "loggedin" not in session or not session["loggedin"]:
        return redirect(url_for("home"))

    stranica = int(request.args.get("stranica", 1))
    rezultati_po_stranici = 4
    offset = (stranica - 1) * rezultati_po_stranici

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if session["uloga"] == 3:
        cursor.execute(
            """
        SELECT novosti.id, novosti.naziv, kategorije.naziv AS kategorija,
               novosti.sadrzaj, novosti.status, novosti.datum
        FROM novosti
        INNER JOIN kategorije ON novosti.kategorija = kategorije.id
        WHERE novosti.id_autora = %s
        ORDER BY novosti.datum DESC
        LIMIT %s OFFSET %s
        """,
            (session["id"], rezultati_po_stranici, offset),
        )
    elif session["uloga"] == 2:
        cursor.execute(
            """
        SELECT DISTINCT novosti.id, novosti.naziv, kategorije.naziv AS kategorija,
               novosti.sadrzaj, novosti.status, novosti.datum
        FROM novosti
        INNER JOIN kategorije ON novosti.kategorija = kategorije.id
        INNER JOIN novinari_kategorije ON novinari_kategorije.kategorija_id = kategorije.id
        WHERE novinari_kategorije.novinar_id = %s
        ORDER BY novosti.datum DESC
        LIMIT %s OFFSET %s
        """,
            (session["id"], rezultati_po_stranici, offset),
        )
    else:
        cursor.execute(
            """
        SELECT novosti.id, novosti.naziv, kategorije.naziv AS kategorija,
               novosti.sadrzaj, novosti.status, novosti.datum
        FROM novosti
        INNER JOIN kategorije ON novosti.kategorija = kategorije.id
        ORDER BY novosti.datum DESC
        LIMIT %s OFFSET %s
        """,
            (rezultati_po_stranici, offset),
        )
    novosti = cursor.fetchall()

    return render_template(
        "pregled_novosti.html",
        novosti=novosti,
        stranica=stranica,
        rezultati_po_stranici=rezultati_po_stranici,
    )


@app.route("/cms/zatrazi_odobrenje/<int:vest_id>")
def zatrazi_odobrenje(vest_id):
    if "loggedin" not in session or not session["loggedin"]:
        return redirect(url_for("home"))

    id_autora = session["id"]

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT naziv FROM novosti WHERE id = %s", (vest_id,))
    vest = cursor.fetchone()

    if not vest:
        return redirect(url_for("pregled_novosti"))

    cursor.execute(
        "SELECT * FROM zahtevi WHERE id_autora = %s AND id_novosti = %s AND zahtev = 'Odobrenje'",
        (id_autora, vest_id),
    )
    existing_request = cursor.fetchone()

    if existing_request:
        return redirect(url_for("pregled_novosti"))

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    zahtev = "Odobrenje"

    cursor.execute(
        """
        INSERT INTO zahtevi (id_autora, id_novosti, datum, zahtev)
        VALUES (%s, %s, %s, %s)
        """,
        (id_autora, vest_id, date, zahtev),
    )
    mysql.connection.commit()

    return redirect(url_for("pregled_novosti"))


@app.route("/cms/zatrazi_izmenu/<int:vest_id>", methods=["GET"])
def zatrazi_izmenu(vest_id):
    if "loggedin" not in session or not session["loggedin"]:
        return redirect(url_for("home"))

    id_autora = session["id"]

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT naziv FROM novosti WHERE id = %s", (vest_id,))
    vest = cursor.fetchone()

    if not vest:
        return redirect(url_for("pregled_novosti"))

    zahtev_tip = request.args.get("zahtev")

    if zahtev_tip not in ["Izmena", "Brisanje"]:
        return redirect(url_for("pregled_novosti"))

    cursor.execute(
        "SELECT * FROM zahtevi WHERE id_autora = %s AND id_novosti = %s AND zahtev = %s",
        (id_autora, vest_id, zahtev_tip),
    )
    existing_request = cursor.fetchone()

    if existing_request:
        return redirect(url_for("pregled_novosti"))

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO zahtevi (id_autora, id_novosti, datum, zahtev)
        VALUES (%s, %s, %s, %s)
        """,
        (id_autora, vest_id, date, zahtev_tip),
    )
    mysql.connection.commit()

    return redirect(url_for("pregled_novosti"))


@app.route("/cms/prikaz_zahteva", methods=["GET", "POST"])
def prikaz_zahteva():
    if "loggedin" not in session or not session["loggedin"] or session["uloga"] == 3:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()
    if session["uloga"] == 1:
        cursor.execute("SELECT * FROM zahtevi")
    else:
        cursor.execute(
            """SELECT zahtevi.*
FROM zahtevi
INNER JOIN novosti ON zahtevi.id_novosti = novosti.id
INNER JOIN novinari_kategorije ON novosti.kategorija = novinari_kategorije.kategorija_id
WHERE novinari_kategorije.novinar_id = %s;""",
            (session["id"],),
        )

    zahtevi = cursor.fetchall()

    return render_template("prikaz_zahteva.html", zahtevi=zahtevi)


@app.route(
    "/cms/odobri_zahtev/<int:id_zahteva>/<string:tip_zahteva>", methods=["GET", "POST"]
)
def odobri_zahtev(id_zahteva, tip_zahteva):
    if "loggedin" not in session or not session["loggedin"] or session["uloga"] == 3:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()

    if tip_zahteva == "Odobrenje":
        cursor.execute(
            "UPDATE novosti n JOIN zahtevi z ON n.id = z.id_novosti SET n.status = 1 WHERE z.id = %s",
            (id_zahteva,),
        )
    elif tip_zahteva == "Izmena":
        cursor.execute(
            "UPDATE novosti n JOIN zahtevi z ON n.id = z.id_novosti SET n.status = 0 WHERE z.id = %s",
            (id_zahteva,),
        )
    else:
        return redirect(url_for("prikaz_zahteva"))

    mysql.connection.commit()

    return redirect(url_for("odbij_zahtev", id_zahteva=id_zahteva))


@app.route("/odbij_zahtev/<int:id_zahteva>", methods=["GET", "POST"])
def odbij_zahtev(id_zahteva):
    if "loggedin" not in session or not session["loggedin"] or session["uloga"] == 3:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()

    try:
        cursor.execute("DELETE FROM zahtevi WHERE id = %s", (id_zahteva,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("prikaz_zahteva"))
    except Exception as e:
        print(f"Error: {e}")
        cursor.close()
        return redirect(url_for("prikaz_zahteva"))


@app.route("/najnovije_vesti")
def najnovije_vesti():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            """
            SELECT n.*, COUNT(l.id_vesti) AS lajkovi
            FROM novosti n
            LEFT JOIN lajkovi_vesti l ON n.id = l.id_vesti
            GROUP BY n.id HAVING n.status = 1
            ORDER BY n.datum DESC, lajkovi DESC
            LIMIT 4
        """
        )
        top_likes = cursor.fetchall()
        procesuiraj_sadrzaj_vesti(top_likes)

        cursor.execute(
            """
            SELECT n.*
            FROM novosti n
            INNER JOIN kategorije k ON n.kategorija = k.id
            WHERE k.naziv = 'sport' AND n.status = 1
            ORDER BY n.datum DESC
            LIMIT 1
        """
        )
        sport_news = cursor.fetchall()

        cursor.execute(
            """
            SELECT n.*
            FROM novosti n
            INNER JOIN kategorije k ON n.kategorija = k.id
            WHERE k.naziv = 'politika' AND n.status = 1
            ORDER BY n.datum DESC
            LIMIT 1
        """
        )
        politika_news = cursor.fetchall()

        cursor.execute(
            """
            SELECT n.*
            FROM novosti n
            INNER JOIN kategorije k ON n.kategorija = k.id
            WHERE k.naziv = 'tehnologija' AND n.status = 1
            ORDER BY n.datum DESC
            LIMIT 1
        """
        )
        tehnologija_news = cursor.fetchall()

        return render_template(
            "najnovije_vesti.html",
            top_likes=top_likes,
            sport_news=sport_news[0] if sport_news else None,
            politika_news=politika_news[0] if politika_news else None,
            tehnologija_news=tehnologija_news[0] if tehnologija_news else None,
        )

    except Exception as e:
        print(e)
        return redirect(url_for("home"))
    finally:
        cursor.close()


@app.route("/dodeli_kategorije/novinar:<int:novinar_id>", methods=["GET", "POST"])
def dodeli_kategorije(novinar_id):
    if "loggedin" not in session or not session["loggedin"] or session["uloga"] == 3:
        return redirect(url_for("home"))

    cursor = mysql.connection.cursor()

    if request.method == "POST":
        kategorije = request.form.getlist("kategorije")

        cursor.execute(
            "DELETE FROM novinari_kategorije WHERE novinar_id = %s", (novinar_id,)
        )

        for kategorija_id in kategorije:
            cursor.execute(
                "INSERT INTO novinari_kategorije (novinar_id, kategorija_id) VALUES (%s, %s)",
                (novinar_id, kategorija_id),
            )
        mysql.connection.commit()

        return redirect(url_for("zaposleni"))

    cursor.execute("SELECT * FROM accounts WHERE id = %s AND uloga != 1", (novinar_id,))
    novinar = cursor.fetchone()

    if not novinar:
        return redirect(url_for("home"))

    cursor.execute(
        "SELECT kategorije.id, kategorije.naziv FROM kategorije JOIN novinari_kategorije ON kategorije.id = novinari_kategorije.kategorija_id WHERE novinari_kategorije.novinar_id = %s",
        (novinar_id,),
    )
    kategorije_dodeljene_novinaru = cursor.fetchall()
    kategorije_ids = [kategorija[0] for kategorija in kategorije_dodeljene_novinaru]

    cursor.execute("SELECT * FROM kategorije")
    kategorije = cursor.fetchall()

    return render_template(
        "dodeli_kategorije.html",
        novinar=novinar,
        kategorije=kategorije,
        kategorije_dodeljene_novinaru=kategorije_ids,
    )


@app.route("/vrati_u_draft/vest:<int:novost_id>")
def vrati_u_draft(novost_id):
    if "loggedin" not in session or not session["loggedin"] or session["uloga"] == 3:
        return redirect(url_for("home"))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM novosti WHERE id = %s", (novost_id,))
        novost = cursor.fetchone()

        if novost:
            cursor.execute(
                "UPDATE novosti SET status = 0 WHERE id = %s",
                (novost_id,),
            )
            mysql.connection.commit()

            return redirect(url_for("pregled_novosti"))
        else:
            return redirect(url_for("pregled_novosti"))

    except Exception as e:
        print(f"Greska prilikom azuriranja statusa novosti: {e}")
        return redirect(url_for("pregled_novosti"))

    finally:
        cursor.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
