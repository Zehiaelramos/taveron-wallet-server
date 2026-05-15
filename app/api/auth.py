from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, UserLogin, Token
from app.services.auth import AuthService
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UserOut)
async def register(
    user_in: UserCreate, 
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Registra un nuevo usuario en el sistema."""
    auth_service = AuthService(db)
    return await auth_service.register_user(user_in, ip_address=request.client.host)

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    """Inicia sesión y devuelve un token de acceso (Compatible con Swagger)."""
    auth_service = AuthService(db)
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    return await auth_service.login_user(credentials, ip_address=request.client.host)

@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Invalida la sesión (Lado del cliente).
    El servidor registra el evento de salida en la auditoría.
    """
    from app.services.audit import AuditService
    audit = AuditService(db)
    await audit.log_event(
        user_id=current_user.id,
        action="USER_LOGOUT",
        ip_address=request.client.host,
        details="Usuario cerró sesión voluntariamente."
    )
    return {"message": "Sesión cerrada exitosamente. Por favor, elimine el token del lado del cliente."}
