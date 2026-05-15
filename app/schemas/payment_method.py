from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
import re
from datetime import datetime
from app.models.payment_method import PaymentMethodType, PaymentMethodStatus

# Esquema base para lectura
class PaymentMethodBase(BaseModel):
    type: PaymentMethodType
    alias: str = Field(..., min_length=1, max_length=50)
    institution: str = Field(..., min_length=1, max_length=50)
    currency: str = Field("MXN", pattern="^[A-Z]{3}$")

# Esquema para creación (entrada)
class PaymentMethodCreate(PaymentMethodBase):
    identifier: str = Field(..., description="Número de tarjeta, cuenta o CLABE")

    @field_validator("identifier")
    @classmethod
    def validate_identifier(cls, v: str, info):
        # Obtener el tipo de pago del diccionario de datos (si está disponible)
        pm_type = info.data.get("type")
        
        # Eliminar espacios o guiones
        clean_v = re.sub(r"[\s-]", "", v)
        
        if not clean_v.isdigit():
            raise ValueError("El identificador debe contener solo números")

        if pm_type == PaymentMethodType.CARD:
            if len(clean_v) not in [15, 16]:
                raise ValueError("La tarjeta debe tener 15 o 16 dígitos")
        
        elif pm_type == PaymentMethodType.CLABE:
            if len(clean_v) != 18:
                raise ValueError("La CLABE debe tener exactamente 18 dígitos")
                
        return clean_v

# Esquema para respuesta (salida)
class PaymentMethodOut(PaymentMethodBase):
    id: int
    # En el listado devolvemos el dato enmascarado
    masked_identifier: str
    status: PaymentMethodStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Esquema para detalle completo (salida)
class PaymentMethodDetail(PaymentMethodOut):
    # En el detalle devolvemos el dato completo (descifrado)
    full_identifier: str
