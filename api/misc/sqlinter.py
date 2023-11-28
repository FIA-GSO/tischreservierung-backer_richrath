
import sqlite3 #Basispacket von Python
from sqlite3 import Error

class SQLInteractor:

    def __init__(self, db_path):
        """Ini path zur zur DB."""
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Verbinde zur Datenbank."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            return self.connection
        except Error as e:
            print(f"Fehler beim Verbinden den DB: {e}")
            return None

    def close(self):
        """Schließe die Verbindung zur Datenbank."""
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=()):
        """Führe eine SQL-Abfrage aus."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Fehler in SQL-Abfrage: {e}")
            return None

    def fetch_all(self, query, params=()):
        """Rufe alle Ergebnisse einer Abfrage ab."""
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchall()
        return None

    def fetch_one(self, query, params=()):
        """Rufe ein einzelnes Ergebnis einer Abfrage ab."""
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchone()
        return None