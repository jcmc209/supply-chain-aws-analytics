"""
Script para configurar Hive Metastore con tablas externas apuntando a MinIO
Sprint 2 - Migración de Memory a Hive Metastore
"""
import trino
import time
import os
from minio import Minio
from minio.error import S3Error

# Configuración
TRINO_HOST = "localhost"
TRINO_PORT = 8080
TRINO_USER = "admin"
CATALOG = "hive"

MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_BUCKET = "raw"
MINIO_SECURE = False

def wait_for_trino(max_retries=10, delay=3):
    """Esperar a que Trino esté disponible"""
    print("\n1. Verificando disponibilidad de Trino...")
    
    for i in range(max_retries):
        try:
            conn = trino.dbapi.connect(
                host=TRINO_HOST,
                port=TRINO_PORT,
                user=TRINO_USER,
                catalog=CATALOG
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchall()
            cursor.close()
            conn.close()
            print("  [OK] Trino está listo")
            return True
        except Exception as e:
            if i < max_retries - 1:
                print(f"  Intento {i+1}/{max_retries} - Esperando Trino...")
                time.sleep(delay)
            else:
                print(f"  [ERROR] Trino no respondió después de {max_retries} intentos")
                print(f"  Error: {e}")
                return False
    return False

def setup_minio():
    """Crear bucket en MinIO y subir archivo CSV"""
    print("\n2. Configurando MinIO...")
    
    try:
        # Conectar a MinIO
        client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE
        )
        
        # Crear bucket si no existe
        if not client.bucket_exists(MINIO_BUCKET):
            client.make_bucket(MINIO_BUCKET)
            print(f"  [OK] Bucket '{MINIO_BUCKET}' creado")
        else:
            print(f"  [OK] Bucket '{MINIO_BUCKET}' ya existe")
        
        # Subir archivo CSV
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
        CSV_PATH = os.path.join(REPO_ROOT, "data", "dirty", "supply_chain_data_dirty.csv")
        
        if not os.path.exists(CSV_PATH):
            print(f"  [ERROR] Archivo no encontrado: {CSV_PATH}")
            print("  Por favor ejecuta primero: python etl/scripts/make_dirty_dataset.py")
            return False
        
        # Subir a MinIO
        object_name = "supply_chain/supply_chain_data_dirty.csv"
        client.fput_object(
            MINIO_BUCKET,
            object_name,
            CSV_PATH,
            content_type="text/csv"
        )
        print(f"  [OK] Archivo subido a s3a://{MINIO_BUCKET}/{object_name}")
        
        return True
        
    except S3Error as e:
        print(f"  [ERROR] Error de MinIO: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] {type(e).__name__}: {e}")
        return False

def execute_query(cursor, query, description="", show_results=False):
    """Ejecutar una query y opcionalmente mostrar resultado"""
    if description:
        print(f"\n{description}")
    
    try:
        cursor.execute(query)
        
        if show_results:
            try:
                results = cursor.fetchall()
                if results:
                    print(f"  Resultados:")
                    for row in results:
                        print(f"    {row}")
                else:
                    print("  (sin resultados)")
            except:
                pass
        
        print(f"  [OK]")
        return True
        
    except Exception as e:
        print(f"  [ERROR] {type(e).__name__}: {e}")
        return False

def setup_hive_catalog():
    """Crear database y tabla externa en Hive Metastore"""
    print("\n3. Configurando catálogo Hive...")
    
    try:
        conn = trino.dbapi.connect(
            host=TRINO_HOST,
            port=TRINO_PORT,
            user=TRINO_USER,
            catalog=CATALOG
        )
        cursor = conn.cursor()
        
        # 1. Crear base de datos
        execute_query(
            cursor,
            "CREATE SCHEMA IF NOT EXISTS supply_chain_raw_db",
            "  Creando schema supply_chain_raw_db..."
        )
        
        # 2. Eliminar tabla si existe (para recrear)
        execute_query(
            cursor,
            "DROP TABLE IF EXISTS supply_chain_raw_db.raw_supply_chain",
            "  Eliminando tabla existente (si existe)..."
        )
        
        # 3. Crear tabla externa apuntando a MinIO
        # NOTA: Hive CSV solo soporta VARCHAR, lo cual es correcto para capa RAW
        # Los tipos de datos se castean en las queries o en la capa CLEAN
        create_table_query = """
        CREATE TABLE supply_chain_raw_db.raw_supply_chain (
            product_type VARCHAR,
            sku VARCHAR,
            price VARCHAR,
            availability VARCHAR,
            number_of_products_sold VARCHAR,
            revenue_generated VARCHAR,
            customer_demographics VARCHAR,
            stock_levels VARCHAR,
            lead_times VARCHAR,
            order_quantities VARCHAR,
            shipping_times VARCHAR,
            shipping_carriers VARCHAR,
            shipping_costs VARCHAR,
            supplier_name VARCHAR,
            location VARCHAR,
            lead_time VARCHAR,
            production_volumes VARCHAR,
            manufacturing_lead_time VARCHAR,
            manufacturing_costs VARCHAR,
            inspection_results VARCHAR,
            defect_rates VARCHAR,
            transportation_modes VARCHAR,
            routes VARCHAR,
            costs VARCHAR
        )
        WITH (
            external_location = 's3a://raw/supply_chain/',
            format = 'CSV',
            skip_header_line_count = 1
        )
        """
        
        execute_query(
            cursor,
            create_table_query,
            "  Creando tabla externa en Hive Metastore..."
        )
        
        # 4. Verificar tabla creada
        execute_query(
            cursor,
            "SELECT COUNT(*) as total_registros FROM supply_chain_raw_db.raw_supply_chain",
            "  Verificando datos cargados...",
            show_results=True
        )
        
        # 5. Mostrar schema
        execute_query(
            cursor,
            "DESCRIBE supply_chain_raw_db.raw_supply_chain",
            "  Schema de la tabla:",
            show_results=True
        )
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] {type(e).__name__}: {e}")
        return False

def main():
    """Función principal"""
    print("="*70)
    print("Setup Hive Metastore + MinIO (Tablas Externas)")
    print("="*70)
    
    # 1. Esperar a que Trino esté listo
    if not wait_for_trino():
        print("\n[FAIL] No se pudo conectar a Trino")
        return
    
    # 2. Configurar MinIO (crear bucket y subir CSV)
    if not setup_minio():
        print("\n[FAIL] Error configurando MinIO")
        return
    
    # 3. Configurar catálogo Hive
    if not setup_hive_catalog():
        print("\n[FAIL] Error configurando Hive catalog")
        return
    
    print("\n" + "="*70)
    print("[SUCCESS] Setup completado exitosamente")
    print("="*70)
    print("\nPróximos pasos:")
    print("  1. Verifica Trino UI: http://localhost:8080")
    print("  2. Verifica MinIO Console: http://localhost:9001")
    print("  3. Ejecuta queries: python sql/trino/run_validation.py")

if __name__ == "__main__":
    main()
