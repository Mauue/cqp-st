import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()


def init():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Image
           (ID INTEGER PRIMARY KEY     NOT NULL,
           rating  TEXT    NOT NULL,
           url TEXT NOT NULL,
           send BOOLEAN DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Status(
        name TEXT PRIMARY KEY NOT NULL,
        value TEXT NOT NULL
    )
    ''')


def new_img(id, rating, url, filename):
    f = cursor.execute('''SELECT ID FROM Image WHERE ID=%s''' % int(id)).fetchone()
    if f is not None:
        return
    cursor.execute('''INSERT INTO Image (ID, rating, url, filename) \
      VALUES ({}, "{}", "{}", "{}")
    '''.format(int(id), rating, url, filename))
    conn.commit()


def mark_image(id):
    cursor.execute("UPDATE Image SET send=1 WHERE id=%s" % c[0])
    conn.commit()


def get_img_url(rating="Safe", num=1, mark=True):
    result = cursor.execute("SELECT id, url, filename FROM Image"
                            " WHERE rating=\"%s\" AND send=0"
                            " ORDER BY RANDOM() LIMIT %s" % (rating, num)).fetchall()
    if result is not None:
        return [{"url": i[1], "filename": i[2]} for i in result]
    return None


def count_img(rating="Safe"):
    c = cursor.execute(
        "SELECT COUNT(id) FROM Image WHERE rating=\"%s\" AND send=0" % rating).fetchone()
    return c[0]


def get_mark_img():
    c = cursor.execute("SELECT filename FROM Image WHERE send=1").fetchall()
    return [i[0] for i in c]
