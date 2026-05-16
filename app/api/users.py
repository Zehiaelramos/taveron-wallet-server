from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserOut, UserUpdate
from app.models.user import User
from app.core.deps import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.get("/me", response_model=UserOut)
async def read_user_me(current_user: User = Depends(get_current_user)):
    """Obtiene el perfil del usuario autenticado."""
    return current_user

@router.patch("/me", response_model=UserOut)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Actualiza el perfil del usuario autenticado (Nombre completo)."""
    try:
        if user_update.full_name is not None:
            current_user.full_name = user_update.full_name
        
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        return current_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el perfil: {str(e)}")
