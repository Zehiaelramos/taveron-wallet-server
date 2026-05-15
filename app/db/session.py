from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# Crear el motor asíncrono
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=True if settings.ENVIRONMENT == "development" else False,
    future=True
)

# Creador de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Dependencia para obtener la sesión de DB en los endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
