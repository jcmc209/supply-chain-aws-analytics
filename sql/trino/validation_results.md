# Resultados de Validacion RAW - Sprint 2

**Fecha:** 2026-01-23  
**Tabla:** `hive.supply_chain_raw_db.raw_supply_chain`  
**Storage:** `s3a://raw/supply_chain/` (MinIO)

---

## Query 1: Total Registros

```
total_registros: 100
```

---

## Query 2: SKUs Unicos

```
skus_unicos: 100
```

---

## Query 3: Proveedores Unicos

```
proveedores_unicos: 5
```

---

## Query 4: Revenue Total

```
revenue_total     revenue_promedio
   577604.82           5776.05
```

---

## Query 5: Shipping Costs

```
shipping_costs_total  shipping_costs_promedio  nulos
              529.40                     5.46      3
```

---

## Query 6: Top 10 SKUs por Revenue

```
  sku product_type  revenue_total
SKU51     haircare        9866.47
SKU38    cosmetics        9692.32
SKU31     skincare        9655.14
SKU90     skincare        9592.63
 SKU2     haircare        9577.75
SKU32     skincare        9571.55
SKU67     skincare        9473.80
SKU88    cosmetics        9444.74
SKU52     skincare        9435.76
SKU18     haircare        9364.67
```

---

## Query 7: Top Proveedores por Defect Rate

```
supplier_name  defect_rate_promedio  cantidad_productos
   Supplier 1                  7.22                  27
   Supplier 5                  2.67                  18
   Supplier 3                  2.47                  15
   Supplier 2                  2.36                  22
   Supplier 4                  2.34                  18
```

**Insight:** Supplier 1 tiene defect rate 3x superior al resto (7.22% vs ~2.4%)

---

## Query 8: Distribucion por Tipo de Producto

```
product_type  cantidad_registros  revenue_total
    skincare                  40      241628.16
    haircare                  34      174455.39
   cosmetics                  26      161521.27
```

**Insight:** Skincare domina con 40% de productos y 41.8% del revenue

---

## Query 9: Problemas de Calidad de Datos

```
shipping_costs_nulos  defect_rates_invalidos  shipping_costs_negativos
                   3                       1                         1
```

**Total issues:** 5 registros con problemas (5% del dataset)

---

## Query 10: Top Rutas por Costos

```
 routes transportation_modes  cantidad_envios  costos_totales
Route B                 Rail               11         7007.41
Route A                 Rail               14         6790.71
Route B                 Road               12         6338.40
Route A                 Road               11         5934.41
Route A                  Air               11         5800.89
Route B                  Air                7         4464.86
Route C                  Air                7         4196.86
Route B                  Sea                6         3386.03
Route C                 Road                5         2932.70
Route A                  Sea                7         2349.76
```

---

## Query 11: Metricas por Ubicacion

```
 location  proveedores  productos  revenue_total
   Mumbai            5         22      137755.03
  Kolkata            5         25      137077.55
  Chennai            5         20      119142.82
Bangalore            5         18      102601.72
    Delhi            5         15       81027.70
```

---

## Query 12: Inventario por Tipo de Producto

```
product_type  productos  stock_promedio  vendidos_total
    skincare         40           40.20           20731
    haircare         34           48.35           13611
   cosmetics         26           58.65           11757
```

---

## Resumen Ejecutivo

### Metricas Clave

| Metrica | Valor |
|---------|-------|
| Total registros | 100 |
| SKUs unicos | 100 |
| Proveedores | 5 |
| Revenue total | $577,604.82 |
| Shipping costs | $529.40 |
| Categorias | 3 (skincare, haircare, cosmetics) |
| Ubicaciones | 5 (Mumbai, Kolkata, Chennai, Bangalore, Delhi) |

### Data Quality Issues

| Issue | Cantidad | % |
|-------|----------|---|
| Shipping costs NULL | 3 | 3% |
| Defect rates > 100 | 1 | 1% |
| Shipping costs < 0 | 1 | 1% |
| **Total** | **5** | **5%** |

### Insights de Negocio

1. **Top Performer:** SKU51 (haircare) - $9,866.47 revenue
2. **Categoria lider:** Skincare (41.8% del revenue total)
3. **Proveedor problematico:** Supplier 1 (7.22% defect rate, 3x promedio)
4. **Ubicacion top:** Mumbai ($137,755 revenue)
5. **Ruta mas costosa:** Route B Rail ($7,007.41)

### Recomendaciones

1. **Urgente:** Revisar calidad de Supplier 1 (alto defect rate)
2. **Media:** Limpiar 5 registros con data quality issues en Sprint 3
3. **Baja:** Evaluar aumentar stock de Skincare (alto revenue, bajo stock)

---

## Comando para Reproducir

```bash
python sql/trino/run_validation.py
```

---

