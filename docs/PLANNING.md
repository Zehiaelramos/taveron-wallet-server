# Hoja de Ruta de Desarrollo (PLANNING.md) 📅

Este documento describe el plan de ejecución para el backend de **Taveron Wallet**, dividido en sprints/fases lógicas.

---

## 🏗 Fase 1: Cimientos y Configuración
**Objetivo:** Tener un entorno funcional con base de datos conectada y estructura de carpetas.

- [x] **1.1 Inicialización de Proyecto**
    - [x] Crear entorno virtual.
    - [x] Instalar dependencias (`requirements.txt`).
    - [x] Configurar variables de entorno (`.env`).
- [x] **1.2 Estructura de Capas**
    - [x] Crear carpetas: `api`, `services`, `repositories`, `models`, `schemas`, `core`.
    - [x] Configurar `main.py` con FastAPI.
- [x] **1.3 Base de Datos**
    - [x] Configurar SQLAlchemy (Async Session).
    - [x] Inicializar Alembic para migraciones.

## 🔐 Fase 2: Autenticación y Usuarios
**Objetivo:** Permitir el registro y login seguro de usuarios.

- [x] **2.1 Modelado de Usuario**
    - [x] Crear modelo SQLAlchemy `User`.
    - [x] Crear esquemas Pydantic para registro/login.
- [x] **2.2 Seguridad de Identidad**
    - [x] Implementar hashing de contraseñas (Bcrypt).
    - [x] Implementar generación y validación de tokens JWT.
- [x] **2.3 Endpoints de Auth**
    - [x] `POST /auth/register`
    - [x] `POST /auth/login`
    - [x] `GET /users/me` (Middleware de autenticación).

## 💳 Fase 3: Wallet y Métodos de Pago
**Objetivo:** CRUD core de la aplicación con manejo de datos sensibles.

- [x] **3.1 Modelado de Pagos**
    - [x] Crear modelo `PaymentMethod` con campos cifrados.
    - [x] Implementar lógica de cifrado/descifrado simétrico (Fernet).
- [x] **3.2 Implementación CRUD**
    - [x] `POST /payment-methods`: Registro con validación de duplicados.
    - [x] `GET /payment-methods`: Listado con enmascaramiento (ej. `**** 1234`).
    - [x] `GET /payment-methods/{id}`: Detalle con dato completo.
    - [x] `DELETE /payment-methods/{id}`: Soft delete.

## 🔍 Fase 4: Trazabilidad y Auditoría
**Objetivo:** Cumplir con el requisito de historial de operaciones.

- [x] **4.1 Modelo de Auditoría**
    - [x] Crear tabla `AuditLog`.
- [x] **4.2 Registro de Eventos**
    - [x] Implementar interceptor o decorador para registrar cambios en métodos de pago.

## 🧪 Fase 5: Refinamiento y Calidad
**Objetivo:** Asegurar que el código es robusto y está documentado.

- [x] **5.1 Validaciones Avanzadas**
    - [x] Validar formatos de tarjeta y CLABE.
- [x] **5.2 Pruebas Unitarias**
    - [x] Testear lógica de cifrado.
    - [x] Testear endpoints de autenticación.
- [x] **5.3 Documentación Final**
    - [x] Revisar Swagger UI.
    - [x] Finalizar README con ejemplos de uso.

## 💎 Fase 6: Pulido Final (Puntos Extra)
**Objetivo:** Implementar detalles de calidad y visualización de arquitectura.

- [x] **6.1 Validación de Duplicados**
    - [x] Evitar que un mismo usuario registre el mismo identificador (tarjeta/cuenta) dos veces.
- [x] **6.2 Paginación y Filtros**
    - [x] Agregar parámetros `skip` y `limit` a los listados de métodos de pago.
- [x] **6.3 Diagrama de Arquitectura**
    - [x] Crear diagrama Mermaid en el README para explicar el flujo de capas y seguridad.
- [x] **6.4 Respuesta de Logout**
    - [x] Documentar el flujo stateless de JWT para el cierre de sesión.

## 🚀 Fase 7: Funcionalidad de Negocio Avanzada
**Objetivo:** Pulir la experiencia de usuario y la seguridad proactiva.

- [x] **7.1 Filtros de Búsqueda**
    - [x] Permitir filtrar el listado de métodos de pago por `type` (card, clabe, etc.).
- [x] **7.2 Gestión de Estatus**
    - [x] Endpoint `PATCH` para activar/desactivar un método de pago sin eliminarlo.
- [x] **7.3 Auditoría de Seguridad Extendida**
    - [x] Registrar en la base de datos los intentos de inicio de sesión fallidos.

---

## 📈 Estado del Proyecto
| Fase | Estado | Progreso |
| :--- | :--- | :--- |
| Fase 1 | ✅ Completado | 100% |
| Fase 2 | ✅ Completado | 100% |
| Fase 3 | ✅ Completado | 100% |
| Fase 4 | ✅ Completado | 100% |
| Fase 5 | ✅ Completado | 100% |
| Fase 6 | ✅ Completado | 100% |
| Fase 7 | ✅ Completado | 100% |

---
**Nota:** Para la implementación del Frontend, consulte el documento [FRONTEND_INSTRUCTIONS.md](FRONTEND_INSTRUCTIONS.md).
