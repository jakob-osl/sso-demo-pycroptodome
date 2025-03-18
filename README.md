# SSO Projekt

Ein Single Sign-On (SSO) System mit zwei Flask-Services: **MyImages** und **MyNotes**.

## Funktionen
- Benutzer können sich bei einem Service einloggen und sind automatisch beim anderen eingeloggt.
- Verschlüsselte Tokens mit AES-GCM.
- Hardcoded Bilder (MyImages) und Notizen (MyNotes) für eingeloggte Benutzer.

## Voraussetzungen
- Python 3.x
- Flask
- PyCryptodome (`pip install pycryptodome`)

## Installation
1. Repository klonen:
   ```bash
   git clone https://github.com/deinusername/sso_project.git
   cd sso_project