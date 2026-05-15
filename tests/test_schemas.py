import pytest
from app.schemas.payment_method import PaymentMethodCreate
from app.models.payment_method import PaymentMethodType

def test_validate_card_ok():
    """Valida que una tarjeta de 16 dígitos pase la validación."""
    data = {
        "type": PaymentMethodType.CARD,
        "alias": "Mi Tarjeta",
        "institution": "BBVA",
        "currency": "MXN",
        "identifier": "1234 5678 1234 5678" # Con espacios
    }
    schema = PaymentMethodCreate(**data)
    assert schema.identifier == "1234567812345678" # Debe salir limpia

def test_validate_card_error():
    """Valida que una tarjeta de longitud errónea falle."""
    data = {
        "type": PaymentMethodType.CARD,
        "alias": "Error",
        "institution": "BBVA",
        "identifier": "123" # Muy corta
    }
    with pytest.raises(ValueError, match="La tarjeta debe tener 15 o 16 dígitos"):
        PaymentMethodCreate(**data)

def test_validate_clabe_ok():
    """Valida que una CLABE de 18 dígitos pase."""
    data = {
        "type": PaymentMethodType.CLABE,
        "alias": "Mi CLABE",
        "institution": "Santander",
        "identifier": "123456789012345678"
    }
    schema = PaymentMethodCreate(**data)
    assert len(schema.identifier) == 18

def test_validate_clabe_error():
    """Valida que una CLABE de longitud errónea falle."""
    data = {
        "type": PaymentMethodType.CLABE,
        "alias": "Error",
        "institution": "Santander",
        "identifier": "12345" # Muy corta
    }
    with pytest.raises(ValueError, match="La CLABE debe tener exactamente 18 dígitos"):
        PaymentMethodCreate(**data)
