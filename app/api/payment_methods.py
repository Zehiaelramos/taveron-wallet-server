from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.payment_method import PaymentMethodType
from app.db.session import get_db
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodOut, PaymentMethodDetail, PaymentMethodStatus
from app.services.payment_method import PaymentMethodService
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/payment-methods", tags=["Métodos de Pago"])

@router.post("/", response_model=PaymentMethodOut, status_code=status.HTTP_201_CREATED)
async def create_pm(
    pm_in: PaymentMethodCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Registra un nuevo método de pago para el usuario autenticado."""
    service = PaymentMethodService(db)
    return await service.create_payment_method(current_user.id, pm_in, ip_address=request.client.host)

@router.get("/", response_model=List[PaymentMethodOut])
async def list_pms(
    skip: int = 0,
    limit: int = 100,
    type: Optional[PaymentMethodType] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos los métodos de pago del usuario (con datos enmascarados, paginación y filtros)."""
    service = PaymentMethodService(db)
    return await service.list_payment_methods(current_user.id, skip=skip, limit=limit, pm_type=type)

@router.get("/{pm_id}", response_model=PaymentMethodDetail)
async def get_pm(
    pm_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene el detalle completo de un método de pago (descifrado)."""
    service = PaymentMethodService(db)
    return await service.get_payment_method_detail(pm_id, current_user.id, ip_address=request.client.host)

@router.patch("/{pm_id}/status", response_model=PaymentMethodOut)
async def update_pm_status(
    pm_id: int,
    status: PaymentMethodStatus,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Activa o desactiva un método de pago."""
    service = PaymentMethodService(db)
    return await service.change_status(pm_id, current_user.id, status, ip_address=request.client.host)

@router.delete("/{pm_id}")
async def delete_pm(
    pm_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina (soft delete) un método de pago."""
    service = PaymentMethodService(db)
    return await service.delete_payment_method(pm_id, current_user.id, ip_address=request.client.host)
