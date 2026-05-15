# Guía de Pruebas y Validación (TESTING.md) 🧪

Este documento detalla los procedimientos para validar la integridad, seguridad y funcionalidad del backend de **Taveron Wallet**.

---

## 1. Pruebas Automatizadas (Pytest)

Hemos implementado un suite de **17 pruebas unitarias e integrales** que utilizan una base de datos **SQLite en memoria**.

### Ejecución de todos los tests:
```powershell
.\venv\Scripts\pytest
```

### Cobertura de Pruebas:
- **`tests/test_encryption.py` (3 tests)**: Valida el cifrado AES/Fernet y el enmascaramiento de datos.
- **`tests/test_auth_api.py` (5 tests)**: 
    - Registro exitoso y bloqueo de duplicados.
    - Login OAuth2 (obtención de JWT).
    - **Logout exitoso** (registro en auditoría).
    - **Manejo de logins fallidos** (auditoría de intentos de intrusión).
- **`tests/test_payment_api.py` (5 tests)**: 
    - Ciclo de vida completo (Crear -> Listar -> Detalle).
    - **Prevención de duplicados** (Blind Indexing).
    - **Filtrado por tipo** (card, clabe, etc.).
    - **Actualización de estatus** (activar/desactivar).
    - **Soft Delete** (borrado lógico).
- **`tests/test_schemas.py` (4 tests)**: 
    - Validación de tarjetas (15/16 dígitos).
    - Validación de CLABE (18 dígitos).
    - Limpieza automática de caracteres.

---

## 2. Validación Manual de Auditoría

El script de consulta rápida permite verificar la trazabilidad de cada acción:
```powershell
$env:PYTHONPATH = "."; .\venv\Scripts\python.exe app/check_logs.py
```
**Nuevos eventos registrados:** `UPDATE_PAYMENT_METHOD_STATUS`, `LOGIN_ATTEMPT_FAILED`.

---

## 3. Validaciones de Negocio (Schemas)

El sistema ahora valida:
- **Duplicados**: No permite registrar el mismo número de cuenta/tarjeta para el mismo usuario.
- **Formato**: Rechaza identificadores que no cumplan con la longitud estándar.

---

## 4. Flujo de Prueba Sugerido en Swagger

1. **Auth**: Registrarse e iniciar sesión.
2. **Filtros**: Registrar una tarjeta y una cuenta CLABE. Consultar `/payment-methods/?type=card` y verificar que solo aparezca la tarjeta.
3. **Estatus**: Desactivar un método con `PATCH /status?status=inactive`. Verificar que en el listado aparezca como inactivo.
4. **Seguridad**: Intentar loguearse con una contraseña falsa y verificar en los logs de auditoría que el intento quedó registrado.

---

## 🔒 Certificación de Seguridad
El backend implementa **Defensa en Profundidad**: Cifrado AES, Hashes determinísticos para búsqueda, Auditoría de eventos y Validaciones de esquema estrictas.
