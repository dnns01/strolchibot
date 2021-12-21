import sqlite3


def get(column):
    conn = sqlite3.connect("db.sqlite3")

    c = conn.cursor()
    c.execute(f"SELECT {column} FROM strolchibot_config")
    value = c.fetchone()[0]
    conn.close()

    return value


def get_bool(column):
    return get(column) == 1


def set(column, value):
    conn = sqlite3.connect("db.sqlite3")

    c = conn.cursor()
    c.execute(f"UPDATE strolchibot_config SET {column}='{value}' where id = 1")
    conn.commit()
    conn.close()
