# Satyam Medya

Data engineering student building batch and streaming pipelines with tests, CI and data-quality checks. Also working on applied ML and LLM security evaluation.

B.Tech CSE (Data Science), Vellore Institute of Technology, graduating 2026. Looking for data engineering internships and entry-level roles.

[satyam.mdya33@gmail.com](mailto:satyam.mdya33@gmail.com) · [LinkedIn](https://www.linkedin.com/in/satyam-medya-2b2825370)

## Projects

Every project runs locally, has a pytest suite, and runs it in GitHub Actions on each push. Datasets are synthetic generators unless noted, so every repo runs without accounts or downloads.

### [airflow-elt-warehouse-pipeline](https://github.com/Satyammedya33/airflow-elt-warehouse-pipeline)
Airflow DAG that extracts raw customer, product and sales data, loads it to staging, and builds a star schema (`dim_customer`, `dim_product`, `dim_date`, `fact_sales`) in PostgreSQL.
- SQL models run in dependency order by a small dbt-style runner (`src/sql_runner.py`).
- Final DAG task runs a quality suite (not-null, unique, accepted-range, referential integrity) and fails the run if any check fails.
- Extract step deliberately injects missing IDs and out-of-range quantities, so the checks are exercised by real failures.

Python · Airflow · PostgreSQL · SQL · Docker Compose

### [realtime-retail-analytics-pipeline](https://github.com/Satyammedya33/realtime-retail-analytics-pipeline)
Streams e-commerce order events through Kafka, aggregates them in 60-second tumbling windows, flags anomalous orders with a rolling z-score, and writes results to PostgreSQL behind a Streamlit dashboard.
- Windowing and scoring logic is separated from Kafka I/O, so it is unit-tested without a broker.

Python · Kafka · PostgreSQL · Streamlit · Docker Compose

### [aws-data-lakehouse-pipeline](https://github.com/Satyammedya33/aws-data-lakehouse-pipeline)
Bronze/silver/gold lakehouse: raw IoT telemetry and clickstream JSON lands in object storage, is cleaned and typed into Parquet, then aggregated into query-ready gold tables queried with DuckDB.
- Terraform defines the AWS side: versioned, encrypted S3 with public access blocked and lifecycle rules, a Glue Data Catalog table, and a least-privilege IAM role.
- Develops against LocalStack, so the full pipeline runs with no AWS bill.

Python · Parquet/Arrow · DuckDB · Terraform · AWS S3/Glue/IAM · LocalStack

### [llm-redteam-safety-framework](https://github.com/Satyammedya33/llm-redteam-safety-framework)
Defensive test harness that runs 12 YAML-defined probes across 7 categories (direct override, role-play jailbreaks, system-prompt extraction, indirect document injection, and more) against an LLM and produces an HTML report.
- Scores with planted canary tokens instead of an LLM judge, so pass/fail is deterministic and reproducible.
- Adapters for OpenAI, Anthropic and an offline mock target; the mock keeps CI free and fast.

Python · OpenAI / Anthropic APIs · YAML · pytest

### [ml-network-intrusion-detection](https://github.com/Satyammedya33/ml-network-intrusion-detection)
Classifies network flows as Normal, DoS, Probe or R2L, comparing Random Forest and XGBoost, with a Streamlit triage view.
- Trained on synthetic NSL-KDD-style flows; the generator is a single module designed to be swapped for the real NSL-KDD or CICIDS2017 CSVs.
- Evaluation reports per-class recall, confusion matrix and ROC-AUC rather than accuracy alone, because missed attacks matter more than overall accuracy.

Python · scikit-learn · XGBoost · pandas · Streamlit

## Skills

- **Languages:** Python, SQL
- **Data:** Apache Airflow, Apache Kafka, PostgreSQL, DuckDB, Parquet/Arrow, pandas
- **Cloud and infra:** Terraform, AWS (S3, Glue, IAM), LocalStack, Docker Compose
- **ML and AI:** scikit-learn, XGBoost, LLM evaluation
- **Practices:** pytest, GitHub Actions CI, data-quality testing
