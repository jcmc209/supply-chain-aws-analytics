# MinIO Structure (S3-compatible Data Lake)

## Purpose
MinIO is used as an S3-compatible object storage to simulate an AWS S3 Data Lake locally.
This project follows a layered Data Lake approach:

- **RAW**: original dataset (as ingested, no transformations)
- **CLEAN**: cleaned/typed dataset (Parquet, partitioned)
- **CURATED**: analytics-ready dataset (BI-ready model)

---

## Access
- MinIO Console (Web UI): http://localhost:9001
- MinIO S3 API endpoint: http://localhost:9000

> Credentials are defined in `infra/.env` (not committed to GitHub).

---

## Buckets / Layers

### raw (Bronze)
**Purpose:** Store original datasets exactly as received.
- No cleaning
- No schema changes
- Full traceability

**Example path:**
- `raw/supply_chain/supply_chain.csv`

---

### clean (Silver)
**Purpose:** Store cleaned and standardized data.
- Converted to Parquet
- Data types fixed
- Null handling applied
- Partitioning strategy applied (for performance)

**Example path:**
- `clean/supply_chain/region=<REGION>/...`
or
- `clean/supply_chain/year=<YYYY>/month=<MM>/...`

---

### curated (Gold)
**Purpose:** Store BI-ready datasets for dashboards and KPI computation.
- Model optimized for analytics
- Ready for SQL queries in Trino

**Example path:**
- `curated/supply_chain/<table_name>/...`

---

## Local Execution (Docker)
MinIO runs locally via Docker Compose.

### Start
From the `infra/` folder:

```bash
docker compose up -d

```

### Stop
From the `infra/` folder:

```bash
docker compose down
```md
