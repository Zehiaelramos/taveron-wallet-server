from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.models.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Acción realizada (ej: "CREATE_PAYMENT_METHOD", "LOGIN", "DELETE_PAYMENT_METHOD")
    action = Column(String, nullable=False)
    
    # Tipo de objeto afectado y su ID
    target_type = Column(String, nullable=True) # ej: "payment_method"
    target_id = Column(String, nullable=True)
    
    # Detalles adicionales en formato texto o JSON
    details = Column(Text, nullable=True)
    
    # Información de red
    ip_address = Column(String, nullable=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
