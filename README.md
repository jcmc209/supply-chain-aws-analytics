# Supply Chain AWS Analytics (End to End)

## Overview
This project builds an end-to-end analytics pipeline using a Supply Chain dataset.
The goal is to simulate a real-world data engineering workflow with a data lake architecture
(raw → clean → curated) and produce business-ready KPIs and dashboards.

Although the pipeline is implemented locally using open-source tools, the architecture is designed
to be **AWS-equivalent**, replicating common AWS analytics services (S3, Glue, Athena) using
S3-compatible storage + a data catalog + SQL query engine.

## Business goal
Answer key supply chain questions such as:
- Which suppliers have the highest delays?
- Which regions generate the highest logistic cost?
- What products generate the most revenue?
- What is the average lead time performance by supplier or region?

## Tech Stack
- MinIO (S3-compatible Data Lake: raw/clean/curated)
- Apache Spark (ETL Jobs)
- Hive Metastore (Data Catalog)
- Trino (SQL Analytics)
- Power BI / Tableau (Dashboards)
  
## Dataset
Kaggle: Supply Chain Analysis Dataset (https://www.kaggle.com/datasets/harshsingh2209/supply-chain-analysis)

### Data Quality Simulation
A dirty dataset version is generated to simulate missing/invalid values:
see `docs/data/dirty_dataset.md`.


## Project Structure
- `docs/` → documentation (architecture, KPIs, data quality)
- `etl/` → Glue scripts / ETL logic
- `sql/` → Athena SQL queries (validation + KPIs)
- `bi/` → dashboards + screenshots
- `assets/` → project screenshots

## Status
**Sprint 2 Completado** ✅

### Sprints
- ✅ **Sprint 1:** Setup + Dataset + Repo + MinIO
- ✅ **Sprint 2:** Catalog RAW + Trino + Data Quality Validation
- 🔄 **Sprint 3:** ETL CLEAN (Glue Job) + Parquet + Particiones  
- ⏳ **Sprint 4:** Curated Layer + Modelo Analítico + KPIs finales
- ⏳ **Sprint 5:** Dashboards + Insights
- ⏳ **Sprint 6:** Empaquetado GitHub + Demo

## Quick Start

```bash
# 1. Levantar servicios (MinIO + Hive Metastore + Trino)
docker-compose -f infra/docker-compose.yml up -d

# 2. Generar dataset dirty (si no existe)
python etl/scripts/make_dirty_dataset.py

# 3. Configurar Hive Metastore + subir datos a MinIO
python etl/scripts/setup_hive_metastore.py

# 4. Ejecutar queries de validación
python sql/trino/run_validation.py
```

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                   Docker Stack (4 servicios)                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐      ┌────────────────┐     ┌──────────────┐ │
│  │  MinIO   │ ←──→ │ Hive Metastore │ ←─→ │  PostgreSQL  │ │
│  │  :9000   │      │     :9083      │     │    :5432     │ │
│  │ (S3 raw) │      │   (metadata)   │     │ (metastore)  │ │
│  └────┬─────┘      └───────┬────────┘     └──────────────┘ │
│       │                    │                               │
│       └────────────┬───────┘                               │
│                    ↓                                       │
│              ┌───────────┐                                 │
│              │   Trino   │                                 │
│              │   :8080   │                                 │
│              │ (queries) │                                 │
│              └───────────┘                                 │
└─────────────────────────────────────────────────────────────┘
```

### Equivalencia AWS

| Componente Local | Servicio AWS |
|------------------|--------------|
| MinIO | S3 |
| Hive Metastore | Glue Data Catalog |
| Trino | Athena |
| PostgreSQL | RDS / Glue Backend |

## Servicios Disponibles

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Trino UI | http://localhost:8080 | - |
| MinIO Console | http://localhost:9001 | minioadmin / minioadmin |
| Hive Metastore | thrift://localhost:9083 | - |
| PostgreSQL | localhost:5432 | hive / hive |