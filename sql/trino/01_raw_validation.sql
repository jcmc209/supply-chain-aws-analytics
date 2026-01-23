/*
====================================================================
SQL RAW VALIDATION QUERIES - Sprint 2
====================================================================
Catalog: hive (Hive Metastore)
Schema: supply_chain_raw_db
Table: raw_supply_chain (External Table -> s3a://raw/supply_chain/)
Fecha: 2026-01-23

NOTA: Los datos RAW se almacenan como VARCHAR (texto).
      Se usa CAST/TRY_CAST para convertir a tipos numericos.
      TRY_CAST retorna NULL si la conversion falla (datos invalidos).
====================================================================
*/

-- 1. Total de registros en la tabla RAW
SELECT COUNT(*) as total_registros
FROM hive.supply_chain_raw_db.raw_supply_chain;

-- 2. Cantidad de SKUs unicos
SELECT COUNT(DISTINCT sku) as skus_unicos
FROM hive.supply_chain_raw_db.raw_supply_chain;

-- 3. Cantidad de proveedores unicos
SELECT COUNT(DISTINCT supplier_name) as proveedores_unicos
FROM hive.supply_chain_raw_db.raw_supply_chain;

-- 4. Revenue total generado
SELECT 
    ROUND(SUM(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_total,
    ROUND(AVG(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_promedio,
    ROUND(MIN(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_minimo,
    ROUND(MAX(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_maximo
FROM hive.supply_chain_raw_db.raw_supply_chain;

-- 5. Costos de envio totales y promedio
SELECT 
    ROUND(SUM(TRY_CAST(shipping_costs AS DOUBLE)), 2) as shipping_costs_total,
    ROUND(AVG(TRY_CAST(shipping_costs AS DOUBLE)), 2) as shipping_costs_promedio,
    COUNT(*) FILTER (WHERE shipping_costs IS NULL OR TRIM(shipping_costs) = '') as shipping_costs_nulos
FROM hive.supply_chain_raw_db.raw_supply_chain;

-- 6. Top 10 SKUs por revenue generado
SELECT 
    sku,
    product_type,
    ROUND(SUM(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_total,
    COUNT(*) as cantidad_registros
FROM hive.supply_chain_raw_db.raw_supply_chain
GROUP BY sku, product_type
ORDER BY revenue_total DESC
LIMIT 10;

-- 7. Top proveedores por defect rate promedio (ordenados de peor a mejor)
SELECT 
    supplier_name,
    location,
    COUNT(*) as cantidad_productos,
    ROUND(AVG(TRY_CAST(defect_rates AS DOUBLE)), 2) as defect_rate_promedio,
    ROUND(MIN(TRY_CAST(defect_rates AS DOUBLE)), 2) as defect_rate_min,
    ROUND(MAX(TRY_CAST(defect_rates AS DOUBLE)), 2) as defect_rate_max
FROM hive.supply_chain_raw_db.raw_supply_chain
GROUP BY supplier_name, location
HAVING COUNT(*) >= 1
ORDER BY defect_rate_promedio DESC
LIMIT 15;

-- 8. Distribucion de registros por tipo de producto
SELECT 
    product_type,
    COUNT(*) as cantidad_registros,
    ROUND(SUM(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_total,
    ROUND(AVG(TRY_CAST(price AS DOUBLE)), 2) as precio_promedio
FROM hive.supply_chain_raw_db.raw_supply_chain
GROUP BY product_type
ORDER BY cantidad_registros DESC;

-- 9. Distribucion por ubicacion (Location)
SELECT 
    location,
    COUNT(DISTINCT supplier_name) as cantidad_proveedores,
    COUNT(*) as cantidad_productos,
    ROUND(SUM(TRY_CAST(revenue_generated AS DOUBLE)), 2) as revenue_total,
    ROUND(AVG(TRY_CAST(defect_rates AS DOUBLE)), 2) as defect_rate_promedio
FROM hive.supply_chain_raw_db.raw_supply_chain
GROUP BY location
ORDER BY revenue_total DESC;

-- 10. Analisis de calidad de datos (Data Quality)
SELECT 
    COUNT(*) as total_registros,
    -- Campos con valores nulos o vacios
    COUNT(*) FILTER (WHERE shipping_costs IS NULL OR TRIM(shipping_costs) = '') as shipping_costs_nulos,
    COUNT(*) FILTER (WHERE manufacturing_costs IS NULL OR TRIM(manufacturing_costs) = '') as manufacturing_costs_nulos,
    COUNT(*) FILTER (WHERE defect_rates IS NULL OR TRIM(defect_rates) = '') as defect_rates_nulos,
    -- Defect rates invalidos (>100)
    COUNT(*) FILTER (WHERE TRY_CAST(defect_rates AS DOUBLE) > 100) as defect_rates_invalidos,
    -- Costos negativos
    COUNT(*) FILTER (WHERE TRY_CAST(shipping_costs AS DOUBLE) < 0) as shipping_costs_negativos,
    COUNT(*) FILTER (WHERE TRY_CAST(manufacturing_costs AS DOUBLE) < 0) as manufacturing_costs_negativos,
    -- Transportation modes variantes
    COUNT(DISTINCT transportation_modes) as transportation_modes_variantes
FROM hive.supply_chain_raw_db.raw_supply_chain;

-- 11. Top rutas por costos logisticos
SELECT 
    routes,
    transportation_modes,
    COUNT(*) as cantidad_envios,
    ROUND(SUM(TRY_CAST(costs AS DOUBLE)), 2) as costos_totales,
    ROUND(AVG(TRY_CAST(costs AS DOUBLE)), 2) as costo_promedio,
    ROUND(AVG(TRY_CAST(shipping_times AS DOUBLE)), 2) as tiempo_envio_promedio_dias
FROM hive.supply_chain_raw_db.raw_supply_chain
GROUP BY routes, transportation_modes
ORDER BY costos_totales DESC
LIMIT 10;

-- 12. Metricas de inventario y disponibilidad
SELECT 
    product_type,
    COUNT(*) as cantidad_productos,
    ROUND(AVG(TRY_CAST(stock_levels AS DOUBLE)), 2) as stock_promedio,
    ROUND(AVG(TRY_CAST(availability AS DOUBLE)), 2) as disponibilidad_promedio,
    CAST(SUM(TRY_CAST(number_of_products_sold AS BIGINT)) AS BIGINT) as productos_vendidos_total
FROM hive.supply_chain_raw_db.raw_supply_chain
GROUP BY product_type
ORDER BY productos_vendidos_total DESC;
