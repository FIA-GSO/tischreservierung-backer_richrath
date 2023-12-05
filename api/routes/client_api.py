from flask import Blueprint, request, jsonify, g
from misc.sqlinter import SQLInteractor
import sqlite3

client_blueprint = Blueprint('client_api', __name__)
DATABASE = '../freieTische.db'

def get_db():
    """Stelle eine Verbindung zur Datenbank her und speichere sie in g."""
    if 'db' not in g:
        g.db = SQLInteractor(DATABASE)
        g.db.connect()
    return g.db


@client_blueprint.teardown_app_request
def close_db(e):
    """Schließe die Datenbankverbindung sauber."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Client API -> Freie Tische anfragen -> Methode: GET -> Pfad: [api.py router]/tische
###
# Request Parameter:
#  - zeitpunkt: Der Zeitpunkt, zu dem die Tische frei sein sollen
# Response:
#  - JSON-Array mit freien Tischen
#  - Beispiel:
#    [
#      {
#        "tischnummer": 1,
#        "anzahlPlaetze": 4
#      },
#      {
#        "tischnummer": 2,
#        "anzahlPlaetze": 6
#      }
#    ]
###
@client_blueprint.route('/tische', methods=['GET'])
def freie_tische_anfragen():
    zeitpunkt = request.args.get('zeitpunkt')
    
    query = """
    SELECT t.tischnummer, t.anzahlPlaetze
    FROM tische t
    LEFT JOIN reservierungen r ON t.tischnummer = r.tischnummer AND r.zeitpunkt = ? AND r.storniert = 'False'
    WHERE r.reservierungsnummer IS NULL
    """
    freie_tische = get_db().fetch_all(query, (zeitpunkt,))
    
    return jsonify(freie_tische)

@client_blueprint.route('/tische/reservieren', methods=['POST'])
def tisch_reservieren():
    zeitpunkt = request.json['zeitpunkt']
    tischnummer = request.json['tischnummer']
    pin = request.json['pin']
    
    query = """
    INSERT INTO reservierungen (zeitpunkt, tischnummer, pin, storniert)
    VALUES (?, ?, ?, 'False')
    """
    get_db().execute_query(query, (zeitpunkt, tischnummer, pin))
    
    return jsonify({'message': 'Tisch reserviert'}), 201

@client_blueprint.route('/tische/<int:reservierungsnummer>', methods=['PUT'])
def reservierung_stornieren(reservierungsnummer):
    pin = request.args.get('pin')
    
    # Überprüfe den PIN
    check_query = "SELECT pin FROM reservierungen WHERE reservierungsnummer = ?"
    actual_pin = get_db().fetch_one(check_query, (reservierungsnummer,))
    
    if not actual_pin or int(actual_pin[0]) != int(pin):
        return jsonify({'message': 'Falscher PIN'}), 403
    
    # Storniere die Reservierung
    query = "UPDATE reservierungen SET storniert = 'True' WHERE reservierungsnummer = ?"
    get_db().execute_query(query, (reservierungsnummer,))
    
    return jsonify({'message': 'Reservierung storniert'})
