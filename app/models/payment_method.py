from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
import enum

class PaymentMethodType(str, enum.Enum):
    CARD = "card"
    BANK_ACCOUNT = "bank_account"
    CLABE = "clabe"
    OTHER = "other"

class PaymentMethodStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    type = Column(SqlEnum(PaymentMethodType), nullable=False)
    alias = Column(String, nullable=False)  # Ej: "Tarjeta de nómina"
    institution = Column(String, nullable=False)  # Ej: "BBVA"
    currency = Column(String, default="MXN")
    
    # Este campo almacenará el número de tarjeta/cuenta cifrado
    encrypted_identifier = Column(String, nullable=False)
    
    # Hash determinístico (SHA-256) para búsqueda de duplicados
    identifier_hash = Column(String, index=True, nullable=True)
    
    status = Column(SqlEnum(PaymentMethodStatus), default=PaymentMethodStatus.ACTIVE)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Soporte para Soft Delete
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relación con el usuario
    user = relationship("User", back_populates="payment_methods")

# Necesitamos actualizar el modelo User para incluir la relación inversa
