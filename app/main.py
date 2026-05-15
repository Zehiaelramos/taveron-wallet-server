from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, payment_methods

app = FastAPI(
    title="Taveron Wallet API",
    description="Backend para la gestión segura de métodos de pago",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(payment_methods.router)

@app.get("/")
async def index():
    return {
        "message": "Bienvenido a Taveron Wallet API",
        "docs": "/docs",
        "status": "online"
    }
