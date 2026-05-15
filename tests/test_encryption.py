import pytest
from app.core.encryption import encrypt_data, decrypt_data, mask_identifier

def test_encryption_decryption():
    """Valida que un dato cifrado pueda recuperarse íntegramente."""
    original_text = "4111222233334444"
    encrypted = encrypt_data(original_text)
    
    assert encrypted != original_text
    assert len(encrypted) > len(original_text)
    
    decrypted = decrypt_data(encrypted)
    assert decrypted == original_text

def test_mask_identifier():
    """Valida que el enmascaramiento oculte todo menos los últimos 4 dígitos."""
    card = "1234567890123456"
    masked = mask_identifier(card)
    
    assert masked == "**** 3456"
    assert "1234" not in masked

def test_encryption_different_values():
    """Valida que el cifrado sea consistente."""
    text = "secret"
    enc1 = encrypt_data(text)
    enc2 = encrypt_data(text)
    
    # Fernet usa un token diferente cada vez (con timestamp), 
    # pero ambos deben descifrar lo mismo.
    assert decrypt_data(enc1) == text
    assert decrypt_data(enc2) == text
