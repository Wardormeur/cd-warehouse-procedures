import json
from psycopg2.extensions import AsIs

with open('./config/config.json') as data:
    data = json.load(data)
regional_bodies = data['regional_bodies']

def insert_users(cursor):
    cursor.execute('CREATE ROLE regional_bodies')
    cursor.execute('GRANT CONNECT ON DATABASE "cdDataWarehouse" TO regional_bodies')
    cursor.execute('GRANT SELECT ON ALL TABLES IN SCHEMA public TO regional_bodies')
    for user in regional_bodies:
        cursor.execute('CREATE USER %s WITH PASSWORD %s', (AsIs(user['name']), user['password'],))
        cursor.execute('GRANT regional_bodies TO %s;', (AsIs(user['name']),))

def drop_users(cursor):
    cursor.execute('SELECT 1 FROM pg_roles WHERE rolname=\'regional_bodies\'')
    if not cursor.fetchone() is None :
        # This needs to be executed from inside the database as the ownership is db dependent
        cursor.execute('DROP OWNED by regional_bodies CASCADE')
        for user in regional_bodies:
            cursor.execute('SELECT 1 FROM pg_roles WHERE rolname=%s', (user['name'],))
            if not cursor.fetchone() is None:
                cursor.execute('DROP USER IF EXISTS %s', (AsIs(user['name']),))
        cursor.execute('DROP ROLE regional_bodies')
