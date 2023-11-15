import sqlite3


def get_result(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute("""
                    DELETE FROM films
                WHERE genre = (SELECT id FROM genres WHERE title = 'боевик') AND
                duration > 90
                    """)
    con.commit()
    con.close()
get_result('films_db.sqlite')