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


def new_img(id, rating, url):
    f = cursor.execute('''SELECT ID FROM Image WHERE ID=%s''' % int(id)).fetchone()
    if f is not None:
        return
    cursor.execute('''INSERT INTO Image (ID, rating, url) \
      VALUES ({}, "{}", "{}")
    '''.format(int(id), rating, url))
    conn.commit()


def get_img_url(rating="Safe", mark=True):
    c = cursor.execute("SELECT id, url FROM Image"
                       " WHERE rating=\"%s\" AND send=0"
                       " ORDER BY RANDOM() LIMIT 1" % rating).fetchone()
    if c is not None:
        if mark:
            cursor.execute("UPDATE Image SET send=1 WHERE id=%s" % c[0])
            conn.commit()
        return c[1]
    return None


def count_img(rating="Safe"):
    c = cursor.execute("SELECT COUNT(id) FROM Image WHERE rating=\"%s\" AND send=0" % rating).fetchone()
    return c[0]


