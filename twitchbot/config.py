import sqlite3


def get_value(key):
    conn = sqlite3.connect("db.sqlite3")

    c = conn.cursor()
    c.execute('SELECT value from strolchibot_config where key = ?', (key,))
    value = c.fetchone()[0]
    conn.close()

    return value


def get_int(key):
    return int(get_value(key))


def get_float(key):
    return float(get_value(key))
