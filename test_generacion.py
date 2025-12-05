import asyncio
import logging
from datetime import date
from src.core.database import AsyncSessionLocal, engine, Base
from src.data.models import Empresa, Empleado
from src.domain.services import GestorLegajosService

# Configuramos logging para ver qué pasa
logging.basicConfig(level=logging.INFO)

async def test_workflow():
    print("\n🚀 INICIANDO TEST DE INTEGRACIÓN: BASE DE DATOS -> TYPST -> PDF\n")


    # 1. Asegurar que las tablas existan (por si borraste la DB)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        try:
            print("--- PASO 1: Creando Datos de Prueba ---")

            
            # A. Crear Empresa Dummy
            # Usamos un CUIT random para que no choque con uniques si corres el test varias veces
            # O borra la DB antes de correr el test.

            import random
            cuit_random = f"30-{random.randint(10000000, 99999999)}-{random.randint(0,9)}"
            

            empresa = Empresa(
                razon_social=f"Construcciones Test {random.randint(1, 100)} S.A.",
                cuit=cuit_random,

                convenio="UOCRA 76/75",
                calle="Av. Siempreviva",
                numero=742,
                localidad="Springfield",
                provincia="Buenos Aires",
                codigo_postal="1000",
                telefono="11-5555-5555",
                mail="rrhh@test.com"

            )

            session.add(empresa)
            await session.flush() # Hacemos flush para obtener el ID de la empresa sin cerrar la transacción

            # B. Crear Empleado Dummy
            dni_random = str(random.randint(10000000, 99999999))
            empleado = Empleado(
                empresa_id=empresa.id,
                nombre="Homero J.",

                apellido="Thompson",
                dni=dni_random,
                cuil=f"20-{dni_random}-0",

                sexo="Masculino",

                nacionalidad="Argentino",

                fecha_nacimiento=date(1980, 5, 12),
                numero_legajo="L-001",

                fecha_ingreso=date(2024, 1, 1),
                sueldo=850000.50,
                categoria="Oficial Especializado",
                obra_social="OSECAC",
                calle="Calle Falsa",
                numero=123,
                localidad="Springfield",
                codigo_postal="5151",

                provincia="Buenos Aires",
                telefono="11-4444-4444"
            )

            session.add(empleado)
            await session.commit()
            print(f"✅ Datos Creados: Empleado ID {empleado.id} en Empresa ID {empresa.id}")


            # --- PASO 2: PROBAR EL SERVICIO ---
            print("\n--- PASO 2: Invocando al Gestor de Legajos (Typst) ---")
            
            # Instanciamos el servicio pasándole la sesión
            gestor_service = GestorLegajosService(session)
            
            # Llamamos a la función mágica
            ruta_pdf = await gestor_service.generar_contrato_empleado(empleado.id)

            
            if ruta_pdf:
                print(f"\n✨ ¡ÉXITO TOTAL! ✨")
                print(f"El documento se generó correctamente en:\n👉 {ruta_pdf}")

                print("Ve a esa carpeta y abre el PDF para verificar que los datos se vean bien.")
            else:
                print("\n❌ FALLO: El servicio retornó None (Revisa los logs de error arriba).")

        except Exception as e:
            print(f"\n💀 ERROR FATAL DURANTE EL TEST: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_workflow())
