from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

# Esquema compartido (Base)
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    full_name: Optional[str] = Field(None, description="Nombre completo del usuario")

# Esquema para crear un usuario (Registro)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Contraseña de al menos 8 caracteres")

# Esquema para actualizar un usuario
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

# Esquema para devolver datos al cliente (Response)
class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Esquema para Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Esquema para el Token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
