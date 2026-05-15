import asyncio
from sqlalchemy import text
from app.db.session import AsyncSessionLocal

async def check_audit_logs():
    print("📜 Consultando Registros de Auditoría...\n")
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT id, action, target_type, timestamp, ip_address FROM audit_logs ORDER BY timestamp DESC LIMIT 10")
        )
        logs = result.fetchall()
        
        if not logs:
            print("⚠️ No hay registros de auditoría aún. Realiza alguna acción en Swagger primero.")
            return

        print(f"{'ID':<4} | {'ACCIÓN':<25} | {'OBJETO':<15} | {'IP':<15}")
        print("-" * 70)
        for log in logs:
            print(f"{log.id:<4} | {log.action:<25} | {str(log.target_type):<15} | {str(log.ip_address):<15}")

if __name__ == "__main__":
    asyncio.run(check_audit_logs())
