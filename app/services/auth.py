from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.services.audit import AuditService
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
        self.audit = AuditService(db)

    async def register_user(self, user_in: UserCreate, ip_address: str = None):
        # 1. Verificar si el usuario ya existe
        user_exists = await self.repository.get_by_email(user_in.email)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )
        
        # 2. Hashear la contraseña
        hashed_password = get_password_hash(user_in.password)
        
        # 3. Guardar en la DB
        user = await self.repository.create(user_in, hashed_password)

        # 4. Auditoría
        await self.audit.log_event(
            user_id=user.id,
            action="USER_REGISTER",
            target_type="user",
            target_id=str(user.id),
            details=f"Usuario registrado: {user.email}",
            ip_address=ip_address
        )
        return user

    async def login_user(self, credentials: UserLogin, ip_address: str = None) -> Token:
        # 1. Buscar usuario
        user = await self.repository.get_by_email(credentials.email)
        if not user:
            # Auditoría de intento de login con email inexistente
            await self.audit.log_event(
                user_id=None,
                action="LOGIN_ATTEMPT_FAILED",
                details=f"Intento de login con email no registrado: {credentials.email}",
                ip_address=ip_address
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas."
            )
        
        # 2. Verificar contraseña
        if not verify_password(credentials.password, user.hashed_password):
            # Auditoría de fallo de login (opcional)
            await self.audit.log_event(
                user_id=user.id,
                action="LOGIN_FAILED",
                details=f"Intento fallido de login para: {user.email}",
                ip_address=ip_address
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas."
            )
        
        # 3. Generar Token
        access_token = create_access_token(subject=user.email)

        # 4. Auditoría de éxito
        await self.audit.log_event(
            user_id=user.id,
            action="USER_LOGIN",
            ip_address=ip_address
        )
        return Token(access_token=access_token, token_type="bearer")
