import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()


def init():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Image
           (ID INTEGER PRIMARY KEY     NOT NULL,
           rating  TEXT    NOT NULL,
           url TEXT NOT NULL,
           send BOOLEAN DEFAULT 0)''')


def new_img(id, rating, url):
    f = cursor.execute('''SELECT ID FROM Image WHERE ID=%s''' % id).fetchone()
    if f is not None:
        return
    cursor.execute('''INSERT INTO Image (ID, rating, url) \
      VALUES ({}, "{}", "{}")
    '''.format(id, rating, url))
    conn.commit()


def get_img(rating="Safe"):
    c = cursor.execute("SELECT id, url FROM Image WHERE rating=\"%s\" AND send=0" % rating).fetchone()
    if c is not None:
        print(c[0], c[1])
        cursor.execute("UPDATE Image SET send=1 WHERE id=%s" % c[0])
        conn.commit()