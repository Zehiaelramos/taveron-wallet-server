import hashlib
from cryptography.fernet import Fernet
from app.core.config import settings

# Inicializar el motor de cifrado con la llave del .env
fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    """Cifra una cadena de texto."""
    if not data:
        return data
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Descifra una cadena de texto cifrada."""
    if not encrypted_data:
        return encrypted_data
    try:
        return fernet.decrypt(encrypted_data.encode()).decode()
    except Exception:
        # En caso de error (llave incorrecta o dato corrupto), devolvemos un aviso
        return "[ERROR AL DESCIFRAR]"

def mask_identifier(identifier: str) -> str:
    """Oculta parte del identificador para mostrar solo los últimos 4 dígitos."""
    if not identifier or len(identifier) < 4:
        return "****"
    return f"**** {identifier[-4:]}"

def generate_hash(data: str) -> str:
    """Genera un hash determinístico (SHA-256) para búsqueda de duplicados."""
    if not data:
        return data
    return hashlib.sha256(data.encode()).hexdigest()
