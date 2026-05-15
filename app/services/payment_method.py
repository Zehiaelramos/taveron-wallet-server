from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.payment_method import PaymentMethodRepository
from app.services.audit import AuditService
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodOut, PaymentMethodDetail
from app.core.encryption import encrypt_data, decrypt_data, mask_identifier, generate_hash

class PaymentMethodService:
    def __init__(self, db: AsyncSession):
        self.repository = PaymentMethodRepository(db)
        self.audit = AuditService(db)

    async def create_payment_method(self, user_id: int, pm_in: PaymentMethodCreate, ip_address: str = None):
        # 1. Generar Hash para detectar duplicados
        id_hash = generate_hash(pm_in.identifier)
        
        # 2. Verificar duplicados
        existing_pm = await self.repository.get_by_hash(user_id, id_hash)
        if existing_pm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Este método de pago ya está registrado con el alias: {existing_pm.alias}"
            )

        # 3. Cifrar el identificador para almacenamiento
        encrypted_id = encrypt_data(pm_in.identifier)
        
        # 4. Guardar en la DB
        db_pm = await self.repository.create(user_id, pm_in, encrypted_id, id_hash)
        
        # 5. Auditoría
        await self.audit.log_event(
            user_id=user_id,
            action="CREATE_PAYMENT_METHOD",
            target_type="payment_method",
            target_id=str(db_pm.id),
            details=f"Creado método de pago: {db_pm.alias} ({db_pm.type})",
            ip_address=ip_address
        )
        
        return self._map_to_out(db_pm)

    async def list_payment_methods(self, user_id: int, skip: int = 0, limit: int = 100, pm_type: str = None):
        db_pms = await self.repository.get_by_user(user_id, skip=skip, limit=limit, pm_type=pm_type)
        return [self._map_to_out(pm) for pm in db_pms]

    async def get_payment_method_detail(self, pm_id: int, user_id: int, ip_address: str = None):
        db_pm = await self.repository.get_by_id(pm_id, user_id)
        if not db_pm:
            raise HTTPException(status_code=404, detail="Método de pago no encontrado")
        
        await self.audit.log_event(
            user_id=user_id,
            action="VIEW_PAYMENT_METHOD_DETAIL",
            target_type="payment_method",
            target_id=str(db_pm.id),
            ip_address=ip_address
        )
        
        full_id = decrypt_data(db_pm.encrypted_identifier)
        
        return PaymentMethodDetail(
            id=db_pm.id,
            type=db_pm.type,
            alias=db_pm.alias,
            institution=db_pm.institution,
            currency=db_pm.currency,
            status=db_pm.status,
            created_at=db_pm.created_at,
            masked_identifier=mask_identifier(full_id),
            full_identifier=full_id
        )

    async def change_status(self, pm_id: int, user_id: int, new_status: str, ip_address: str = None):
        db_pm = await self.repository.get_by_id(pm_id, user_id)
        if not db_pm:
            raise HTTPException(status_code=404, detail="Método de pago no encontrado")
        
        updated_pm = await self.repository.update_status(db_pm, new_status)
        
        # Auditoría del cambio de estatus
        await self.audit.log_event(
            user_id=user_id,
            action="UPDATE_PAYMENT_METHOD_STATUS",
            target_type="payment_method",
            target_id=str(db_pm.id),
            details=f"Estatus cambiado a: {new_status} para {db_pm.alias}",
            ip_address=ip_address
        )
        
        return self._map_to_out(updated_pm)

    async def delete_payment_method(self, pm_id: int, user_id: int, ip_address: str = None):
        db_pm = await self.repository.get_by_id(pm_id, user_id)
        if not db_pm:
            raise HTTPException(status_code=404, detail="Método de pago no encontrado")
        
        await self.repository.soft_delete(db_pm)
        
        await self.audit.log_event(
            user_id=user_id,
            action="DELETE_PAYMENT_METHOD",
            target_type="payment_method",
            target_id=str(db_pm.id),
            details=f"Eliminado (soft delete) método de pago: {db_pm.alias}",
            ip_address=ip_address
        )
        
        return {"message": "Método de pago eliminado correctamente"}

    def _map_to_out(self, db_pm) -> PaymentMethodOut:
        """Helper para convertir modelo DB a esquema de salida con máscara."""
        full_id = decrypt_data(db_pm.encrypted_identifier)
        return PaymentMethodOut(
            id=db_pm.id,
            type=db_pm.type,
            alias=db_pm.alias,
            institution=db_pm.institution,
            currency=db_pm.currency,
            status=db_pm.status,
            created_at=db_pm.created_at,
            masked_identifier=mask_identifier(full_id)
        )
