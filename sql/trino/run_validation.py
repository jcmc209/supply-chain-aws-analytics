"""
Script para ejecutar las queries de validación RAW y guardar resultados
"""
import trino
import pandas as pd
from datetime import datetime

# Trino config
TRINO_HOST = "localhost"
TRINO_PORT = 8080
TRINO_USER = "admin"
CATALOG = "hive"

def run_query(cursor, query_name, query_sql):
    """Ejecutar query y mostrar resultados"""
    print(f"\n{'='*70}")
    print(f"QUERY: {query_name}")
    print(f"{'='*70}")
    
    try:
        cursor.execute(query_sql)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        df = pd.DataFrame(results, columns=columns)
        print(df.to_string(index=False))
        print(f"\nFilas retornadas: {len(df)}")
        return df
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

def main():
    print("="*70)
    print("VALIDACION DE DATOS RAW - SPRINT 2")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Conectar
    conn = trino.dbapi.connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        user=TRINO_USER,
        catalog=CATALOG
    )
    cursor = conn.cursor()
    
    # Queries (usando TRY_CAST porque los datos RAW son VARCHAR)
    queries = {
        "1. Total registros": """
            SELECT COUNT(*) as total_registros
            FROM hive.supply_chain_raw_db.raw_supply_chain
        """,
        
        "2. SKUs unicos": """
            SELECT COUNT(DISTINCT sku) as skus_unicos
            FROM hive.supply_chain_raw_db.raw_supply_chain
        """,
        
        "3. Proveedores unicos": """
            SELECT COUNT(DISTINCT supplier_name) as proveedores_unicos
            FROM hive.supply_chain_raw_db.raw_supply_chain
        """,
        
        "4. Revenue total": """
            SELECT 
                ROUND(SUM(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_total,
                ROUND(AVG(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_promedio
            FROM hive.supply_chain_raw_db.raw_supply_chain
        """,
        
        "5. Shipping costs": """
            SELECT 
                ROUND(SUM(TRY_CAST(shipping_costs AS DOUBLE)), 2) as shipping_costs_total,
                ROUND(AVG(TRY_CAST(shipping_costs AS DOUBLE)), 2) as shipping_costs_promedio,
                COUNT(*) FILTER (WHERE shipping_costs IS NULL OR TRIM(shipping_costs) = '') as nulos
            FROM hive.supply_chain_raw_db.raw_supply_chain
        """,
        
        "6. Top 10 SKUs por revenue": """
            SELECT 
                sku,
                product_type,
                ROUND(SUM(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_total
            FROM hive.supply_chain_raw_db.raw_supply_chain
            GROUP BY sku, product_type
            ORDER BY revenue_total DESC
            LIMIT 10
        """,
        
        "7. Top proveedores por defect rate": """
            SELECT 
                supplier_name,
                ROUND(AVG(TRY_CAST(defect_rates AS DOUBLE)), 2) as defect_rate_promedio,
                COUNT(*) as cantidad_productos
            FROM hive.supply_chain_raw_db.raw_supply_chain
            GROUP BY supplier_name
            ORDER BY defect_rate_promedio DESC
            LIMIT 10
        """,
        
        "8. Distribucion por tipo de producto": """
            SELECT 
                product_type,
                COUNT(*) as cantidad_registros,
                ROUND(SUM(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_total
            FROM hive.supply_chain_raw_db.raw_supply_chain
            GROUP BY product_type
            ORDER BY cantidad_registros DESC
        """,
        
        "9. Problemas de calidad de datos": """
            SELECT 
                COUNT(*) FILTER (WHERE shipping_costs IS NULL OR TRIM(shipping_costs) = '') as shipping_costs_nulos,
                COUNT(*) FILTER (WHERE TRY_CAST(defect_rates AS DOUBLE) > 100) as defect_rates_invalidos,
                COUNT(*) FILTER (WHERE TRY_CAST(shipping_costs AS DOUBLE) < 0) as shipping_costs_negativos
            FROM hive.supply_chain_raw_db.raw_supply_chain
        """,
        
        "10. Top rutas por costos": """
            SELECT 
                routes,
                transportation_modes,
                COUNT(*) as cantidad_envios,
                ROUND(SUM(TRY_CAST(costs AS DOUBLE)), 2) as costos_totales
            FROM hive.supply_chain_raw_db.raw_supply_chain
            GROUP BY routes, transportation_modes
            ORDER BY costos_totales DESC
            LIMIT 10
        """,
        
        "11. Metricas por ubicacion": """
            SELECT 
                location,
                COUNT(DISTINCT supplier_name) as proveedores,
                COUNT(*) as productos,
                ROUND(SUM(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_total
            FROM hive.supply_chain_raw_db.raw_supply_chain
            GROUP BY location
            ORDER BY revenue_total DESC
        """,
        
        "12. Inventario por tipo de producto": """
            SELECT 
                product_type,
                COUNT(*) as productos,
                ROUND(AVG(TRY_CAST(stock_levels AS DOUBLE)), 2) as stock_promedio,
                CAST(SUM(TRY_CAST(number_of_products_sold AS BIGINT)) AS BIGINT) as vendidos_total
            FROM hive.supply_chain_raw_db.raw_supply_chain
            GROUP BY product_type
            ORDER BY vendidos_total DESC
        """
    }
    
    # Ejecutar queries
    for name, sql in queries.items():
        run_query(cursor, name, sql)
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*70)
    print("VALIDACION COMPLETADA")
    print("="*70)

if __name__ == "__main__":
    main()
