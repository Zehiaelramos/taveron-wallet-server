from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.audit import AuditRepository

class AuditService:
    def __init__(self, db: AsyncSession):
        self.repository = AuditRepository(db)

    async def log_event(
        self, 
        user_id: int, 
        action: str, 
        target_type: str = None, 
        target_id: str = None, 
        details: str = None,
        ip_address: str = None
    ):
        """Lógica para registrar un evento de auditoría."""
        return await self.repository.create_log(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
            ip_address=ip_address
        )
