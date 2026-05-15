# **Prueba técnica - Wallet segura de métodos de pago**

## **Objetivo**

Desarrollar una aplicación web tipo **wallet**, donde una persona pueda crear una cuenta, iniciar sesión y administrar sus métodos de pago de forma segura.

La prueba busca evaluar habilidades fullstack, criterio técnico, diseño de base de datos, desarrollo de APIs, frontend, arquitectura, seguridad, trazabilidad, validaciones y manejo responsable de información sensible.

## **Tiempo estimado**

La prueba está pensada para desarrollarse en aproximadamente **3 días**.

## **Tecnologías**

El candidato puede elegir las tecnologías específicas, respetando las siguientes condiciones:

- Backend en **Python**.
- Frontend en **JavaScript**.
- Base de datos libre de tipo sql preferiblemente.
- Se valorará documentación clara, pruebas automatizadas y facilidad para levantar el proyecto.

## **Funcionalidades requeridas**

La aplicación debe permitir:

- Registro de usuario.
- Inicio y cierre de sesión.
- Consulta del perfil del usuario autenticado.
- Registro de métodos de pago.
- Listado de métodos de pago del usuario autenticado.
- Consulta de detalle de un método de pago.
- Eliminación o desactivación de un método de pago.
- Prevención de registros duplicados.
- Registro de trazabilidad para operaciones relevantes.

## **Métodos de pago**

Cada método de pago debe contener información básica como:

- Tipo de método: tarjeta, cuenta bancaria, CLABE u otro.
- Alias.
- Institución.
- Moneda.
- Identificador del método de pago.
- Estatus.

El sistema debe considerar que algunos de estos datos pueden ser sensibles, por lo que se espera un manejo cuidadoso tanto en backend como en frontend.

## **Frontend**

El frontend debe incluir las pantallas necesarias para usar el flujo principal de la aplicación:

- Registro.
- Login.
- Perfil o vista principal.
- Listado de métodos de pago.
- Alta de método de pago.
- Detalle de método de pago.
- Eliminación o desactivación.

No se evaluará diseño visual avanzado, pero sí claridad, organización, experiencia de uso y manejo adecuado de errores.

## **Entregables**

El candidato deberá entregar:

- Repositorio con backend y frontend, deseable en github.
- Instrucciones para levantar el proyecto.
- Migraciones o script de base de datos.
- Archivo .env.example.
- README con explicación general de la solución.

## **Evaluación**

Se evaluará principalmente:

- Cumplimiento funcional.
- Seguridad y privacidad.
- Calidad de arquitectura.
- Calidad de código.
- Diseño de base de datos.
- Validaciones.
- Manejo de errores.
- Trazabilidad.
- Frontend funcional.
- Documentación.
- Pruebas.

## **Puntos adicionales**

Se valorará positivamente, sin ser obligatorio:

- Pruebas automatizadas.
- Paginación o filtros.
- Soft delete.
- Separación clara por capas.
- Diagrama simple de arquitectura.
- Documentación más detallada.
- Buen manejo de configuración por ambiente.

## **Consideraciones**

No es necesario implementar pagos reales, transferencias, saldos, integración bancaria, recuperación de contraseña, 2FA, roles avanzados ni despliegue en la nube.

Tampoco se requiere desarrollar un sistema de autenticación personalizado desde cero o algún otro sistema de seguridad. Es suficiente utilizar el mecanismo de autenticación y manejo de sesiones proporcionado por la tecnología o framework elegido, siempre que esté correctamente aplicado dentro de la solución.