# uvozimo ustrezne podatke za povezavo
import uvoz.auth as auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import csv

def ustvari_tabelo():
    cur.execute("""
    CREATE TABLE oseba (
        emso SERIAL UNIQUE PRIMARY KEY,
        ime TEXT NOT NULL,
        priimek TEXT NOT NULL,
        email TEXT NOT NULL unique,
        naslov TEXT NOT NULL,
        regija TEXT NOT NULL,
        telefon INTEGER         
    );
    """) 
    conn.commit()

def pobrisi_tabelo():
    cur.execute("""
        DROP TABLE oseba;
    """)
    conn.commit()

def uvozi_podatke():
    with open("podatki/osebe.csv", encoding="utf-16", errors='ignore') as f:
        rd = csv.reader(f)
        next(rd) # izpusti naslovno vrstico
        for r in rd:
            cur.execute("""
                INSERT INTO oseba
                (emso,ime,priimek,email,naslov,regija,telefon)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, r)
            print("Uvožena oseba %s z ID-jem %s" % (r[1], r[0]))
    conn.commit()


conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

# pobrisi_tabelo()
# ustvari_tabelo()
uvozi_podatke()