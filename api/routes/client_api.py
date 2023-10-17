from flask import Blueprint, request, jsonify, g
from misc.sqlinter import SQLInteractor
import sqlite3

client_blueprint = Blueprint('kellner_api', __name__)
DATABASE = 'pfad_zur_deiner_datenbank.db'

def get_db():
    """Stelle eine Verbindung zur Datenbank her und speichere sie in g."""
    if 'db' not in g:
        g.db = SQLInteractor(DATABASE)
        g.db.connect()
    return g.db


@client_blueprint.teardown_appcontext
def close_db(e):
    """Schließe die Datenbankverbindung sauber."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Kellner API
@client_blueprint.route('/freieTische', methods=['GET'])
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

@client_blueprint.route('/reservieren', methods=['POST'])
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

@client_blueprint.route('/stornieren/<int:reservierungsnummer>', methods=['PUT'])
def reservierung_stornieren(reservierungsnummer):
    pin = request.json['pin']
    
    # Überprüfe den PIN
    check_query = "SELECT pin FROM reservierungen WHERE reservierungsnummer = ?"
    actual_pin = get_db().fetch_one(check_query, (reservierungsnummer,))
    
    if not actual_pin or actual_pin[0] != pin:
        return jsonify({'message': 'Falscher PIN'}), 403
    
    # Storniere die Reservierung
    query = "UPDATE reservierungen SET storniert = 'True' WHERE reservierungsnummer = ?"
    get_db().execute_query(query, (reservierungsnummer,))
    
    return jsonify({'message': 'Reservierung storniert'})
