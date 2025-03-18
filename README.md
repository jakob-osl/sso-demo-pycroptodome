# SSO Project

This project implements a Single Sign-On (SSO) system with two Flask-based web services: **MyImages** and **MyNotes**. The system allows users to authenticate once and access both services concurrently using a shared, cryptographically secure token.

## Project Structure
- `src/`
  - `shared/`: Shared modules used by both services.
    - `crypto.py`: Implements token generation and verification using AES-GCM.
    - `database.py`: Simulates a shared user database.
  - `myimages/`: First web service displaying images for authenticated users.
    - `app.py`: Flask application for MyImages.
    - `static/`: Static files (CSS and images).
    - `templates/`: HTML templates.
  - `mynotes/`: Second web service displaying notes for authenticated users.
    - `app.py`: Flask application for MyNotes.
    - `static/`: Static files (CSS).
    - `templates/`: HTML templates.

## Features
- **Single Sign-On (SSO)**: Users log in to one service (e.g., MyImages) and are automatically authenticated in the other (e.g., MyNotes) via a shared token stored in a browser cookie.
- **Token Security**: Tokens are encrypted and authenticated using AES-GCM with a random nonce.
- **Concurrent Services**: The fictional service "MyImages" runs on port 5000, "MyNotes" on port 5001, both as separate Flask instances.

## Prerequisites
- Python 3.8 or higher
- Flask (pip install flask)
- PyCryptodome (pip install pycryptodome)

## Installation
Clone the repository:

```shell
git clone https://github.com/yourusername/sso_project.git
cd sso_project
```
   
Install dependencies:

```shell
pip install -r requirements.txt
```

## Usage
Initialize the database

```shell
cd src/shared
python database.py
```

Then start the MyImages service which will run on http://localhost:5000:

```shell
cd src/myimages
python app.py
```

Then start the MyNotes service in a separate terminal which will run on http://localhost:5001:

```shell
cd src/mynotes
python app.py
```
   
Finally open your browser:
   - Go to http://localhost/login.
   - Log in with username "testuser" and password "password".
   - After successful login, visit http://localhost:5001/ to see automatic authentication.
   - Log out from either service to end the session on both.

## Implementation Choices
### Technology
- Flask: Chosen for its simplicity and flexibility in building lightweight web services.
- SQLite: Chosen for its simplicity.
- Note: The creation of the Webservices, HTML and CSS boilerplate was assisted by GenAI.

### Cryptography
- AES-GCM: Used for token encryption and authentication. AES in GCM mode provides both confidentiality (via encryption) and integrity (via an authentication tag). Therefore, we don't need a separate MAC.
  - Key: A 16-byte AES key is hardcoded in the in the cryptography module for the sake of this exercise
  - Nonce: A random 12-byte nonce is generated for each token to prevent replay attacks and ensure uniqueness.
  - Header: A dynamic header (b"Service 1" or b"Service 2") is included in the token as Associated Data, authenticated but not encrypted. This binds the token to the SSO context.
  - Token Format: header:nonce:ciphertext:tag, encoded in Base64, stored in a cookie for browser sharing.

### Token Management
- Cookie-Based: The token is stored in an HTTP cookie (auth_token) with a 30-minute lifetime.
- Session: Flask’s session is used to track the authenticated user’s state locally within each service.

### Web Services
- MyImages: Displays images which are visible only to authenticated users.
- MyNotes: Displays notes which are visible only to authenticated users.

### Comment on the lack of web-security mechanisms
- No HTTPS: For simplicity, the project uses HTTP locally. In production, HTTPS should be enabled.
- Cookie Flags: Currently missing secure, httponly, and samesite flags, which should be added to mitigate XSS and CSRF risks.
- There are certainly more flaws but as described in the task, we put the focus on the cryptographical solution instead of the web-security mechanisms.
