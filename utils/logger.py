import logging 
import os 
from .encryption import encrypt_bytes, decrypt_bytes

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'audit.log')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('audit')

def log_action(user, action, target=None):
    entry = f"{user} | {action} | {target}\n".encode()
    secured = encrypt_bytes(entry)
    with open(LOG_PATH, 'ab') as f:
        f.write(secured)

def read_logs();
    with open(LOG_PATH, 'rb') as f:
        for token in f:
            print(decrypt_bytes(token).decode())
