<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="100%" alt="Satyam Medya — data engineer and data analyst. Streaming, orchestrated ELT and cloud lakehouse pipelines. Tested, CI-checked, reproducible.">
</picture>

<sub>
  <a href="mailto:satyam.mdya33@gmail.com">satyam.mdya33@gmail.com</a> ·
  <a href="https://www.linkedin.com/in/satyam-medya-2b2825370">LinkedIn</a> ·
  Open to data engineering internships and entry-level roles ·
  B.Tech CSE (Data Science), VIT, 2026
</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg">
  <img src="assets/stats-light.svg" width="100%" alt="5 pipelines, 34 automated tests, 5 of 5 repos tested in CI, 0 cloud accounts needed to run them.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <img src="assets/stack-light.svg" width="100%" alt="Tech stack. Languages: Python, SQL, Java, C, C++. Data engineering: Kafka, Airflow, Parquet, DuckDB, plus ETL/ELT design, dbt-style SQL modelling, star-schema warehousing and data-quality validation. Cloud and DevOps: AWS (S3, Glue, Athena, IAM), Terraform, Docker, LocalStack, GitHub Actions. Data and ML: pandas, NumPy, scikit-learn, XGBoost, TensorFlow, Keras, Jupyter. Databases and BI: PostgreSQL, MySQL, Power BI, Excel. Security: LLM prompt-injection red-teaming, network intrusion detection, applied ML for security.">
</picture>

<table>
<tr>
<td width="50%" valign="top">
  <a href="https://github.com/Satyammedya33/airflow-elt-warehouse-pipeline"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-airflow-dark.svg">
    <img src="assets/card-airflow-light.svg" width="100%" alt="Airflow ELT Warehouse: orchestrated ELT from raw operational data to a PostgreSQL star schema. Pipeline: extract, load, SQL models, quality gate. 3 dimensions plus 1 fact table built by dependency-ordered dbt-style SQL models. The final DAG task runs not-null, unique, range and referential-integrity checks and fails the run on any violation. Source data deliberately contains invalid rows, so the gate is tested against real failures. Airflow, PostgreSQL, SQL, Docker Compose, 7 tests.">
  </picture></a>
  <a href="https://github.com/Satyammedya33/airflow-elt-warehouse-pipeline/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/Satyammedya33/airflow-elt-warehouse-pipeline/ci.yml?branch=main&style=flat-square&label=CI&labelColor=161B22&color=30363D" alt="CI status"></a>
</td>
<td width="50%" valign="top">
  <a href="https://github.com/Satyammedya33/realtime-retail-analytics-pipeline"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-retail-dark.svg">
    <img src="assets/card-retail-light.svg" width="100%" alt="Real-Time Retail Analytics: event streaming with live metrics and in-flight anomaly detection. Pipeline: Kafka, 60-second windows, z-score, Postgres. Revenue, order count and average order value per 60-second tumbling window. A rolling z-score flags anomalous order amounts as they stream through. Windowing and scoring are pure functions, unit-tested without a broker; the full stack runs in Docker Compose. Kafka, PostgreSQL, Streamlit, Docker Compose, 8 tests.">
  </picture></a>
  <a href="https://github.com/Satyammedya33/realtime-retail-analytics-pipeline/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/Satyammedya33/realtime-retail-analytics-pipeline/ci.yml?branch=main&style=flat-square&label=CI&labelColor=161B22&color=30363D" alt="CI status"></a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
  <a href="https://github.com/Satyammedya33/aws-data-lakehouse-pipeline"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-lakehouse-dark.svg">
    <img src="assets/card-lakehouse-light.svg" width="100%" alt="AWS Data Lakehouse: medallion lakehouse for IoT telemetry and clickstream events. Pipeline: bronze, silver, gold, DuckDB SQL. Terraform provisions versioned, encrypted S3 with public access blocked, lifecycle rules, a Glue catalog and a least-privilege IAM role. The same code runs on local disk, LocalStack or real S3, switched by one environment variable. The silver layer types data into Parquet and drops faulty sensor readings. Terraform, AWS, Parquet, DuckDB, LocalStack, 3 tests.">
  </picture></a>
  <a href="https://github.com/Satyammedya33/aws-data-lakehouse-pipeline/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/Satyammedya33/aws-data-lakehouse-pipeline/ci.yml?branch=main&style=flat-square&label=CI&labelColor=161B22&color=30363D" alt="CI status"></a>
</td>
<td width="50%" valign="top">
  <a href="https://github.com/Satyammedya33/llm-redteam-safety-framework"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-llm-dark.svg">
    <img src="assets/card-llm-light.svg" width="100%" alt="LLM Red-Team Framework: a defensive harness measuring how well an LLM resists manipulation. Pipeline: probes, target, canary scoring, report. 12 probes across 7 categories including prompt injection, jailbreaks and system-prompt extraction. Deterministic canary-token and refusal-pattern scoring, with no LLM judge in the loop. Reference reports in the repo: safe target 100% robust, leaky target 34%; adapters for OpenAI, Anthropic and an offline mock. Python, OpenAI and Anthropic APIs, YAML, 9 tests.">
  </picture></a>
  <a href="https://github.com/Satyammedya33/llm-redteam-safety-framework/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/Satyammedya33/llm-redteam-safety-framework/ci.yml?branch=main&style=flat-square&label=CI&labelColor=161B22&color=30363D" alt="CI status"></a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
  <a href="https://github.com/Satyammedya33/ml-network-intrusion-detection"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-ids-dark.svg">
    <img src="assets/card-ids-light.svg" width="100%" alt="ML Intrusion Detection: classifies network flows as Normal, DoS, Probe or R2L. Pipeline: flows, features, Random Forest or XGBoost, metrics. Random Forest and XGBoost are compared on NSL-KDD-style flow features. Evaluation reports per-class precision, recall and F1, a confusion matrix and ROC-AUC, because a missed attack costs more than a false alarm. The data source is isolated in one module, ready to swap the synthetic generator for real NSL-KDD or CICIDS2017. scikit-learn, XGBoost, pandas, Streamlit, 7 tests.">
  </picture></a>
  <a href="https://github.com/Satyammedya33/ml-network-intrusion-detection/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/Satyammedya33/ml-network-intrusion-detection/ci.yml?branch=main&style=flat-square&label=CI&labelColor=161B22&color=30363D" alt="CI status"></a>
</td>
<td width="50%" valign="top">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/principles-dark.svg">
    <img src="assets/principles-light.svg" width="100%" alt="How I build. Every push is tested: pytest runs in GitHub Actions on each push. Data quality is a gate, not a report: bad data stops the pipeline before it reaches consumers. Infrastructure is code: cloud resources are declared in Terraform, not clicked together. Anyone can run it: Docker Compose, LocalStack and mock adapters mean no cloud bill or API key to evaluate the work. Honest data: where data is synthetic, the README says so.">
  </picture>
</td>
</tr>
</table>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/education-dark.svg">
  <img src="assets/education-light.svg" width="100%" alt="Education. Vellore Institute of Technology, B.Tech Computer Science & Engineering (Data Science), 2021 to 2026. Coursework: Data Structures & Algorithms, DBMS, Operating Systems, Computer Networks, Statistics & Probability. Certifications: Advanced Machine Learning & Python Bootcamp, IoT Architecture (VIT).">
</picture>

<details>
<summary><sub>Plain-text version</sub></summary>

**Satyam Medya** — data engineer / data analyst. B.Tech CSE (Data Science), VIT, 2026. Open to data engineering internships and entry-level roles. [satyam.mdya33@gmail.com](mailto:satyam.mdya33@gmail.com) · [LinkedIn](https://www.linkedin.com/in/satyam-medya-2b2825370)

Five end-to-end projects, each with a pytest suite run by GitHub Actions on every push, and each runnable locally without a cloud account. Datasets are synthetic generators unless noted.

- **[airflow-elt-warehouse-pipeline](https://github.com/Satyammedya33/airflow-elt-warehouse-pipeline)** — Airflow DAG: extract → load → dbt-style SQL models → PostgreSQL star schema (3 dimensions + 1 fact), with a final quality gate (not-null, unique, range, referential integrity) that fails the run on any violation. 7 tests.
- **[realtime-retail-analytics-pipeline](https://github.com/Satyammedya33/realtime-retail-analytics-pipeline)** — Kafka stream: 60-second tumbling-window revenue, order count and AOV, plus rolling z-score anomaly detection into PostgreSQL with a Streamlit dashboard. 8 tests.
- **[aws-data-lakehouse-pipeline](https://github.com/Satyammedya33/aws-data-lakehouse-pipeline)** — bronze/silver/gold medallion lakehouse in Parquet, queried with DuckDB; Terraform provisions versioned, encrypted S3, a Glue catalog and a least-privilege IAM role; runs on local disk, LocalStack or S3. 3 tests.
- **[llm-redteam-safety-framework](https://github.com/Satyammedya33/llm-redteam-safety-framework)** — defensive LLM evaluation: 12 probes across 7 categories, deterministic canary-token and refusal-pattern scoring, HTML reports, adapters for OpenAI, Anthropic and an offline mock. 9 tests.
- **[ml-network-intrusion-detection](https://github.com/Satyammedya33/ml-network-intrusion-detection)** — Random Forest vs XGBoost on NSL-KDD-style flows (Normal/DoS/Probe/R2L), evaluated on per-class recall, confusion matrix and ROC-AUC, with a Streamlit triage dashboard. 7 tests.

**Skills** — Python, SQL, Java, C/C++ · Apache Kafka, Apache Airflow, ETL/ELT design, dbt-style SQL modelling, star-schema warehousing, data-quality validation · AWS (S3, Glue, Athena, IAM), Terraform, Docker & Docker Compose, LocalStack, GitHub Actions · pandas, NumPy, scikit-learn, XGBoost, TensorFlow, Keras · PostgreSQL, MySQL, DuckDB, Parquet/Arrow, Power BI, Excel, Jupyter · LLM/prompt-injection red-teaming, network intrusion detection, applied ML for security

</details>

<sub>Panels on this page are SVGs generated by <a href="scripts/gen_readme.py">scripts/gen_readme.py</a> — Geist (SIL OFL 1.1) subset and embedded, logos from Devicon (MIT) and Simple Icons (CC0).</sub>
