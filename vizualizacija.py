from bottle import *
import hashlib
from datetime import date
from generator_tock import *
from decimal import *


#Privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
ROOT = os.environ.get('BOTTLE_ROOT', '/')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Odkomentiraj, če želiš sporočila o napakah
debug(True)  # za izpise pri razvoju

# Mapa za statične vire (slike, css, ...)
static_dir = "./static"

skrivnost = 'safnju134839safqwr'

@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)

@get('/')
def index():
    return template('zacetna.html')

@post('/podatki')
def podatki_post():
    verjetnost = request.forms.verjetnost
    verjetnost=Decimal(verjetnost)
    cas = request.forms.cas
    cas=int(cas)
    radij = request.forms.radij
    radij=Decimal(radij)
    koraki = request.forms.koraki
    koraki=int(koraki)
    tocke_za_simulacijo = request.forms.tocke_za_simulacijo
    tocke_za_simulacijo = int(tocke_za_simulacijo)
    zacetne = request.forms.zacetne
    zacetne=int(zacetne)
    #tocke = generiraj_n_tock(tocke_za_simulacijo)
    #narisi_m_okuzenih_tock(tocke_za_simulacijo, zacetne, tocke, cas, radij)
    okuzi_sosede(tocke_za_simulacijo, zacetne, verjetnost, cas, 1000, radij, koraki)
    redirect('/')


# reloader=True nam olajša razvoj (ozveževanje sproti - razvoj)
run(host='localhost', port=SERVER_PORT, reloader=RELOADER)