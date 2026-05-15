# Guía de Instalación Detallada (INSTALL.md) 🛠️

Este documento describe los pasos necesarios para configurar el entorno de desarrollo y poner en marcha el backend de **Taveron Wallet**.

---

## 1. Requisitos del Sistema
- **Python 3.10+**: Asegúrate de tener instalado Python y que esté en tu PATH.
- **PostgreSQL**: Se requiere una instancia activa (Local o Docker).
- **Entorno Windows**: Estas instrucciones usan comandos de PowerShell.

## 2. Configuración del Entorno Virtual

```powershell
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual
.\venv\Scripts\activate
```

## 3. Instalación de Dependencias

El proyecto utiliza las siguientes librerías clave instalables via `pip`:

- **FastAPI & Uvicorn**: Para el servidor web asíncrono.
- **SQLAlchemy & Asyncpg**: Para la gestión de base de datos asíncrona.
- **Alembic**: Para las migraciones de esquemas.
- **Python-JOSE & Cryptography**: Para la gestión de seguridad (JWT y Fernet).
- **Bcrypt (v4.0.1)**: Para el hashing seguro de contraseñas.
- **Pydantic v2**: Para validación de esquemas y configuraciones.

Instala todo con:
```powershell
pip install -r requirements.txt
```

## 4. Configuración de Base de Datos y .env

1.  Crea una base de datos en Postgres llamada `taveron`.
2.  Copia el archivo `.env.example` a `.env`:
    ```powershell
    copy .env.example .env
    ```
3.  Edita el archivo `.env` con tus credenciales locales. **Importante:** Asegúrate de generar una `ENCRYPTION_KEY` válida usando el comando comentado dentro del archivo.

## 5. Migraciones y Arranque

```powershell
# Ejecutar las migraciones para crear las tablas
alembic upgrade head

# Iniciar el servidor en modo desarrollo
uvicorn app.main:app --reload
```

El servidor estará disponible en: `http://127.0.0.1:8000`
La documentación Swagger en: `http://127.0.0.1:8000/docs`
