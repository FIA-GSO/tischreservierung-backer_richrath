from flask import Blueprint, request, jsonify, g
from misc.sqlinter import SQLInteractor
import sqlite3


kellner_blueprint = Blueprint('kellner_api', __name__)
DATABASE = '../freieTische.db'

def get_db():
    """Stelle eine Verbindung zur Datenbank her und speichere sie in g."""
    if 'db' not in g:
        g.db = SQLInteractor(DATABASE)
        g.db.connect()
    return g.db

@kellner_blueprint.teardown_app_request
def close_db(e):
    """Schließe die Datenbankverbindung sauber."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Kellner API -> Tischreservierungen einsehen -> Methode: GET -> Pfad: [api.py router]/reservierungen
@kellner_blueprint.route('/reservierungen', methods=['GET'])
def alle_reservierungen_sehen():
    query = "SELECT * FROM reservierungen WHERE storniert = 'False'"
    reservierungen = get_db().fetch_all(query)
    
    return jsonify(reservierungen)