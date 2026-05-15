from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models.payment_method import PaymentMethod, PaymentMethodType
from app.schemas.payment_method import PaymentMethodCreate
from datetime import datetime

class PaymentMethodRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100, pm_type: PaymentMethodType = None):
        """Lista los métodos de pago activos de un usuario, con filtros opcionales."""
        query = select(PaymentMethod).where(
            and_(
                PaymentMethod.user_id == user_id,
                PaymentMethod.deleted_at == None
            )
        )
        
        if pm_type:
            query = query.where(PaymentMethod.type == pm_type)
            
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_hash(self, user_id: int, identifier_hash: str):
        """Busca un método de pago por su hash (para evitar duplicados)."""
        query = select(PaymentMethod).where(
            and_(
                PaymentMethod.user_id == user_id,
                PaymentMethod.identifier_hash == identifier_hash,
                PaymentMethod.deleted_at == None
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, pm_id: int, user_id: int):
        """Obtiene un método de pago específico por ID y Usuario."""
        query = select(PaymentMethod).where(
            and_(
                PaymentMethod.id == pm_id,
                PaymentMethod.user_id == user_id,
                PaymentMethod.deleted_at == None
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user_id: int, pm_in: PaymentMethodCreate, encrypted_id: str, identifier_hash: str) -> PaymentMethod:
        """Registra un nuevo método de pago."""
        db_pm = PaymentMethod(
            user_id=user_id,
            type=pm_in.type,
            alias=pm_in.alias,
            institution=pm_in.institution,
            currency=pm_in.currency,
            encrypted_identifier=encrypted_id,
            identifier_hash=identifier_hash
        )
        self.db.add(db_pm)
        await self.db.commit()
        await self.db.refresh(db_pm)
        return db_pm

    async def update_status(self, db_pm: PaymentMethod, status: str) -> PaymentMethod:
        """Actualiza el estatus (ACTIVE/INACTIVE) de un método de pago."""
        db_pm.status = status
        await self.db.commit()
        await self.db.refresh(db_pm)
        return db_pm

    async def soft_delete(self, db_pm: PaymentMethod):
        """Realiza una eliminación lógica."""
        db_pm.deleted_at = datetime.utcnow()
        await self.db.commit()
        return db_pm
