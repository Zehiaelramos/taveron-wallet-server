from fastapi import APIRouter, Depends
from app.schemas.user import UserOut
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.get("/me", response_model=UserOut)
async def read_user_me(current_user: User = Depends(get_current_user)):
    """Obtiene el perfil del usuario autenticado."""
    return current_user
