import pytest
from flask_testing import TestCase
from unittest.mock import patch
from flask import g
import sys
import os

# Füge das übergeordnete Verzeichnis zum Suchpfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api import create_app, client_blueprint, kellner_blueprint
from routes.client_api import client_blueprint  # Importiere den Client-Blueprint
from routes.kellner_api import kellner_blueprint  # Importiere den Kellner


class UnitTest(TestCase):
    
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        # Registriere die Blueprints in der Test-App
        app.register_blueprint(client_blueprint, url_prefix='/api/v1/client')
        app.register_blueprint(kellner_blueprint, url_prefix='/api/v1/kellner')
        return app.test_client()

    #Teste Default Route ("/" | GET)
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tischreservierung', response.data)


    #Client API Test
    ###############################################################################################################
    @patch('client_api.get_db')
    def test_freie_tische_anfragen(self, mock_get_db):
        # Mocke die Datenbankantwort
        mock_get_db.return_value.fetch_all.return_value = [{'tischnummer': 1, 'anzahlPlaetze': 4}]
        
        response = self.client.get('/api/v1/client/freieTische?zeitpunkt=2022-02-02 17:30:00')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"tischnummer": 2, "anzahlPlaetze": 6}', response.data)

    @patch('client_api.get_db')
    def test_tisch_reservieren(self, mock_get_db):
        response = self.client.post('/api/v1/client/reservieren', json={
            'zeitpunkt': '22022-02-02 17:30:00',
            'tischnummer': 3,
            'pin': 1234
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Tisch reserviert', response.data)

    @patch('client_api.get_db')
    def test_reservierung_stornieren(self, mock_get_db):
        # Mocke die Überprüfung des PINs
        mock_get_db.return_value.fetch_one.return_value = [1234]

        response = self.client.put('/api/v1/client/stornieren/2?pin=1234')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reservierung storniert', response.data)
        
    ##############################################################################################################
    #
    #Kellner API Test
    #
    ###############################################################################################################
    @patch('kellner_api.get_db')
    def test_alle_reservierungen_sehen(self, mock_get_db):
        # Mocke die Datenbankantwort
        mock_get_db.return_value.fetch_all.return_value = [
            {'reservierungsnummer': 1, 'zeitpunkt': '2022-02-02 17:30:00', 'tischnummer': 1, 'pin': 1331, 'storniert': 'False'}
        ]
        
        response = self.client.get('/api/v1/kellner/reservierungen')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"reservierungsnummer": 1, "zeitpunkt": "2022-02-02 17:30:00", "tischnummer": 1, "pin": 1331, "storniert": "False"}', response.data)


# Damit pytest die Tests erkennt
if __name__ == '__main__':
    pytest.main()