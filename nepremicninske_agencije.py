#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottleext import *

# uvozimo ustrezne podatke za povezavo
import auth_public as auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

# Zakomentiraj, če ne želiš sporočil o napakah
debug = True

skrivnost = "rODX3ulHw3ZYRdbIVcp1IfJTDn8iQTH6TFaNBgrSkjIulr"

def nastaviSporocilo(sporocilo = None):
    # global napakaSporocilo
    staro = request.get_cookie("sporocilo", secret=skrivnost)
    if sporocilo is None:
        bottle.Response.delete_cookie(key='sporocilo', path='/', secret=skrivnost)
    else:
        bottle.Response.set_cookie(key='sporocilo', value=sporocilo, path="/", secret=skrivnost)
    return staro 

# Funkcije za izgradnjo strani

# Statične datoteke damo v mapo 'static' in do njih pridemo na naslovu '/static/...'
# Uporabno za slike in CSS, poskusi http://localhost:8080/static/slika.jpg
@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')


#začetna stran 
@get('/')
def hello():
    return 'Začetna stran'

@get('/osebe')
def index():
    cur.execute("""
    SELECT id, ime, priimek, ulica, hisna_stevilka, email, telefon, posta.postna_stevilka , posta.posta FROM oseba
    INNER JOIN posta ON posta.postna_stevilka = oseba.posta_id
    ORDER BY oseba.priimek """)
    return template('oseba.html', osebe=cur)

@get('/posta')
def posta():
    cur.execute("""
        SELECT * FROM posta
    """)
    return template('posta.html', posta=cur)

@get('/nepremicnina')
def nepremicnina():
    cur.execute("""
        SELECT agencija.id, agencija.ime, agencija.mesto, agencija.id FROM nepremicnina
        INNER JOIN agencija ON agencija.id = nepremicnina.kupuje_agencija
    """)
    return template('nepremicnina.html', nepremicnina=cur)

######################################################################
# Glavni program
# tu bi se priklopili na bazo

# Poženemo strežnik na portu 8080, glej http://localhost:8080/
# Iz bottle dokumentacije o parametru reloader=True: Every time you edit a module file, 
# the reloader restarts the server process and loads the newest version of your code. 
conn = psycopg2.connect(database='sem2022_ninav', host='baza.fmf.uni-lj.si', user='javnost', password='javnogeslo')
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogocimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
run(host='localhost', port=8080, reloader=True)

######################################################################