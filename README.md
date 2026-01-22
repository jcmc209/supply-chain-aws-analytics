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
- `etl/` → ETL scripts
- `sql/` → SQL queries (validation + KPIs)
- `bi/` → dashboards + screenshots
- `assets/` → project screenshots

## Status
Work in progress (Sprint-based development).