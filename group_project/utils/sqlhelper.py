import psycopg2
from psycopg2._psycopg import cursor

PG_SQL_LOCAL = {
        'database': 'group11db',
        'user': 'testuser',
        'password': 'xxxx',
        'host': 'localhost',
        'port': '5432',
    }


def get_list(sql, args):
    conn = psycopg2.connect(**PG_SQL_LOCAL)
    cursor = conn.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_one(sql, args):
    conn = psycopg2.connect(**PG_SQL_LOCAL)
    cursor = conn.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def modify(sql, args):
    conn = psycopg2.connect(**PG_SQL_LOCAL)
    cursor = conn.cursor()
    cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()
