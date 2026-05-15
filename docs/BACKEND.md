# Plan de Implementación: Backend Wallet Segura (Python)

Este documento detalla el plan paso a paso para construir el backend de la aplicación **Taveron Wallet**, enfocado en seguridad, trazabilidad y una arquitectura escalable.

## 🛠 Stack Tecnológico Propuesto

- **Lenguaje:** Python 3.10+
- **Framework:** FastAPI (Alto rendimiento, documentación automática con Swagger).
- **Base de Datos:** PostgreSQL (Relacional, ideal para integridad de datos).
- **ORM:** SQLAlchemy con Alembic (Migraciones).
- **Seguridad:** 
    - JWT (JSON Web Tokens) para autenticación.
    - Passlib (bcrypt) para hash de contraseñas.
    - Cryptography (Fernet) para cifrado simétrico de datos sensibles.
- **Validación:** Pydantic.

---

## 🏗 Arquitectura del Proyecto (Layered Architecture)

Para cumplir con el punto adicional de "Separación clara por capas", se propone la siguiente estructura:

```text
app/
├── api/                # Endpoints (Routes)
├── core/               # Configuración, seguridad y constantes
├── models/             # Modelos de Base de Datos (SQLAlchemy)
├── schemas/            # Esquemas de Validación (Pydantic)
├── services/           # Lógica de Negocio (Business Logic)
├── repositories/       # Acceso a datos (CRUD directo)
├── db/                 # Sesión de DB y migraciones
└── main.py             # Punto de entrada
```

---

## 📝 Fases de Desarrollo

### Fase 1: Configuración Inicial
1.  **Entorno:** Inicializar entorno virtual y `requirements.txt`.
2.  **Estructura:** Crear el andamiaje de carpetas.
3.  **DB Setup:** Configurar la conexión a PostgreSQL y sesión asíncrona.
4.  **Config:** Implementar manejo de variables de entorno (`.env`).

### Fase 2: Autenticación y Usuarios
1.  **Modelo User:** `id, email, password_hash, full_name, created_at`.
2.  **Seguridad:** Implementar utilidades para hashing de contraseñas y generación/verificación de JWT.
3.  **Endpoints:**
    - `POST /auth/register`: Registro de nuevos usuarios.
    - `POST /auth/login`: Login y retorno de Token.
    - `GET /users/me`: Perfil del usuario autenticado.

### Fase 3: Gestión de Métodos de Pago
1.  **Modelo PaymentMethod:** 
    - `id, user_id, type (card, bank, clabe), alias, institution, currency, encrypted_identifier, status, created_at, deleted_at`.
2.  **Cifrado de Datos:** Crear servicio para cifrar/descifrar el `encrypted_identifier` (ej. número de tarjeta) en la DB.
3.  **Endpoints:**
    - `POST /payment-methods`: Crear (con validación de duplicados).
    - `GET /payment-methods`: Listar (con filtros y paginación).
    - `GET /payment-methods/{id}`: Detalle (desenmascarando información sensible).
    - `DELETE /payment-methods/{id}`: Soft delete (cambio de status o `deleted_at`).

### Fase 4: Trazabilidad (Audit Logs)
1.  **Modelo AuditLog:** `id, user_id, action, target_type, target_id, timestamp, ip_address`.
2.  **Middleware/Interceptor:** Registrar automáticamente operaciones de escritura (POST, PUT, DELETE).

### Fase 5: Calidad y Entrega
1.  **Validaciones:** Asegurar que los esquemas Pydantic validen formatos (ej. CLABE de 18 dígitos).
2.  **Pruebas:** Implementar pruebas unitarias con `pytest` para los servicios críticos.
3.  **Documentación:** Completar README y asegurar que Swagger (`/docs`) sea descriptivo.

---

## 🔒 Consideraciones de Seguridad
- **Sensitive Data:** Nunca almacenar el identificador del método de pago en texto plano.
- **Masking:** En el listado general, devolver solo los últimos 4 dígitos. Solo en el "detalle" permitir ver el dato completo tras re-autenticación o validación de token.
- **CORS:** Configurar correctamente para permitir solo el dominio del frontend.

---

## 🚀 Próximos Pasos
¿Te gustaría comenzar con la **Fase 1 (Configuración Inicial)** o prefieres ajustar alguna de las tecnologías propuestas?
