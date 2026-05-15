from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

class AuditRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_log(
        self, 
        user_id: int, 
        action: str, 
        target_type: str = None, 
        target_id: str = None, 
        details: str = None,
        ip_address: str = None
    ):
        """Crea un nuevo registro de auditoría."""
        log = AuditLog(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
            ip_address=ip_address
        )
        self.db.add(log)
        await self.db.commit()
        return log
