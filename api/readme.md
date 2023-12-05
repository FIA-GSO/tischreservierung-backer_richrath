# Projektstart-Anleitung

## Voraussetzungen

Bevor du das Projekt startest, stelle sicher, dass die folgenden Voraussetzungen erfüllt sind:

---

### Installation der Abhängigkeiten

Um alle benötigten Pakete zu installieren, führe einen der folgenden Befehle aus:

```bash
pip install -r requirements.txt
```

Falls dabei ein Fehler auftritt, versuche es mit:

```bash
pip3 install -r requirements.txt
```

---

# Projektstart

## Starten des Projektes

Um das Projekt zu starten, führe den folgenden Befehl aus:

```bash
python3 .\api.py
```

**Wichtig**: Stelle sicher, dass du dich im gleichen Verzeichnis wie `api.py` befindest.

## Datenbank

Das Projekt verwendet eine SQLite-Datenbank namens `freieTische.db`. Diese ist notwendig, um Anfragen an das System zu bearbeiten.

--- 

# API-Endpunkte
## Client-Endpunkte
Die Client-Endpunkte sind in der Blueprint client_api.py definiert, welche sich unter `.\routes\client_api.py` befindet.

### Kellner-Endpunkte
Die Kellner-Endpunkte sind in der Blueprint kellner_api.py definiert, welche sich unter `.\routes\kellner_api.py` befindet.

### SQL Interactor
Der SQL Interactor, der für Datenbankinteraktionen verwendet wird, kann unter `.\misc\sqlinter.py` gefunden werden.