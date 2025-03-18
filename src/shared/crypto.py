import base64
import json
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

AES_KEY = b'SixteeenBytesKey'
TIME_TO_LIVE = 1800  # 30 minutes


def generate_token(username: str, header: bytes = b"") -> str:
    # Calculate expiration time
    current_time = time.time()
    expiration_time = current_time + TIME_TO_LIVE

    # Generate random nonce
    nonce = os.urandom(12)

    # Create message
    message = {'username': username, 'exp': expiration_time}
    message_json = json.dumps(message).encode('utf-8')

    # Encrypt message
    padded_message = pad(message_json, block_size=AES.block_size)
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(padded_message)

    # Encode token parts
    token_parts = {
        'header:': base64.b64encode(header).decode('utf-8'),
        'nonce': base64.b64encode(nonce).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'tag': base64.b64encode(tag).decode('utf-8')
    }

    # Token = header:nonce:ciphertext:tag
    token = f"{token_parts['header:']}:{token_parts['nonce']}:{token_parts['ciphertext']}:{token_parts['tag']}"

    return token


def verify_and_decrypt_token(token: str) -> dict:
    try:
        # Split and decode token
        header, nonce, ciphertext, tag = token.split(':')
        header = base64.b64decode(header.encode('utf-8'))
        nonce = base64.b64decode(nonce.encode('utf-8'))
        ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
        tag = base64.b64decode(tag.encode('utf-8'))

        # Decrypt and verify token
        cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
        cipher.update(header)
        message = unpad(cipher.decrypt_and_verify(
            ciphertext, tag), AES.block_size)

        # Parse JSON
        message = json.loads(message)

        # Check expiration time
        if message['exp'] < time.time():
            raise ValueError('Token expired')

        return message

    except ValueError as e:
        raise ValueError(f"Invalid token: {str(e)}")
    except Exception as e:
        raise ValueError('Invalid token: Decryption or parsing failed')
