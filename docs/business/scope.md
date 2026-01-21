# Scope

## In Scope (MVP Deliverables)
- MinIO data lake with layers: raw / clean / curated
- Hive Metastore for raw/clean/curated
- Spark to build clean layer in Parquet + partitioning
- Trino SQL queries: validation + KPIs
- 2 dashboards (Operational + Cost/Supplier)
- Docs: architecture diagram, data quality report, KPI definitions, insights

## Out of Scope
- Streaming (Kinesis/Kafka)
- Orchestration (Airflow/MWAA)
- CI/CD
- Machine Learning
- Production security hardening

## Definition of Done
Project is complete when:
- raw/clean/curated exist in S3
- clean/curated are Parquet + partitioned
- Trino queries run successfully
- dashboards + insights documented in GitHub
