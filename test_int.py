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
    WHERE 1=1
    """

    params = []

    if search_query:
        query += " AND (novosti.naziv LIKE %s OR novosti.sadrzaj LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

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