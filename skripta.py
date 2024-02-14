import random
import datetime
from loremipsum import get_sentences
import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="baze")
cursor = db.cursor()

start_date = datetime.datetime.now() - datetime.timedelta(days=5 * 365)
current_date = start_date

for article_id in range(1, 9126):
    title = f"Članak broj {article_id}"
    category = str(random.choice([1, 5, 6])) 
    content_type = random.choice(["image", "video"])
    author_id = 1
    status = 1
    date = current_date.strftime("%Y-%m-%d %H:%M:%S")
    tags = "lorem, ipsum, demo, tekst"

    if content_type == "image":
        content = f'<p><img src="../static/uploads/test.jpeg" alt="" width="348" height="261"></p>\n'
    else: 
        content = f'<div style="max-width: 650px;" data-ephox-embed-iri="https://youtu.be/a3ICNMQW7Ok">\n'
        content += '<div style="left: 0; width: 100%; height: 0; position: relative; padding-bottom: 56.25%;">'
        content += '<iframe style="top: 0; left: 0; width: 100%; height: 100%; position: absolute; border: 0;" '
        content += 'src="https://www.youtube.com/embed/a3ICNMQW7Ok?rel=0" scrolling="no" '
        content += 'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share;" '
        content += 'allowfullscreen="allowfullscreen"></iframe></div></div>'

    lorem_text = get_sentences(random.randint(5, 10))
    content += "\n".join([f"<p>{sentence}</p>" for sentence in lorem_text])

    cursor.execute(
        "INSERT INTO novosti (naziv, kategorija, sadrzaj, id_autora, status, datum, tagovi) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (title, category, content, author_id, status, date, tags),
    )

    db.commit()

    if article_id % 5 == 0:
        current_date += datetime.timedelta(days=1)

db.close()
