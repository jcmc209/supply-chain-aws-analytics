# Scope

## In Scope (MVP Deliverables)
- AWS S3 data lake with layers: raw / clean / curated
- Glue Crawler for raw/clean/curated
- Glue Job to build clean layer in Parquet + partitioning
- Athena SQL queries: validation + KPIs
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
- Athena queries run successfully
- dashboards + insights documented in GitHub
