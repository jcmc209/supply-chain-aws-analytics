# Supply Chain AWS Analytics (End to End)

## Overview
This project builds an end-to-end analytics pipeline on AWS using a Supply Chain dataset.
The goal is to simulate a real-world data engineering workflow with a data lake architecture
(raw → clean → curated) and produce business-ready KPIs and dashboards.

## Business goal
Answer key supply chain questions such as:
- Which suppliers have the highest delays?
- Which regions generate the highest logistic cost?
- What products generate the most revenue?
- What is the average lead time performance by supplier or region?

## Tech Stack
- AWS S3 (Data Lake: raw/clean/curated)
- AWS Glue (Crawler + ETL Jobs)
- AWS Athena (SQL Analytics)
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
Work in progress (Sprint-based development).