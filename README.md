<div align="center">

<img src="./assets/banner.svg" alt="Satyam Medya — Data Engineer, AI/LLM Safety, Applied Security" width="100%" />

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Satyam%20Medya-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/satyam-medya-2b2825370)
[![Email](https://img.shields.io/badge/Email-satyam.mdya33%40gmail.com-2dd4bf?style=for-the-badge&logo=gmail&logoColor=white)](mailto:satyam.mdya33@gmail.com)
[![Status](https://img.shields.io/badge/Open_to-Data%20Engineer%20%2F%20Analyst%20roles-8b5cf6?style=for-the-badge)](#-lets-connect)
[![Visitors](https://komarev.com/ghpvc/?username=Satyammedya33&style=for-the-badge&color=2dd4bf&label=Profile+Views)](https://github.com/Satyammedya33)

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=16&duration=2600&pause=1000&color=8B93A7&center=true&vCenter=true&width=680&lines=orchestrating+ELT+with+Airflow+%2B+dbt-style+SQL;streaming+fraud+detection+on+Kafka;red-teaming+LLMs+for+prompt-injection+resistance;shipping+lakehouses+on+AWS+with+Terraform" alt="status line" />

</div>

<br/>

## 👋 About me

I'm a data engineer who ships **production-shaped** pipelines, not notebooks — every repo below has Docker, CI, tests, and automated data-quality gates. On the side I dig into the security half of the stack: **red-teaming LLMs** against prompt injection and building **ML classifiers for network intrusion detection**.

- 🎓 B.Tech CSE (Data Science) — Vellore Institute of Technology
- 🔭 Building: streaming, orchestrated ELT, and cloud-lakehouse pipelines with quality gates baked in
- 🛡️ Exploring: AI/LLM safety evaluation and applied ML for network security
- ⚡ Fun fact: every pipeline I ship has to survive its own test suite before it survives production

<br/>

## 🚀 Featured builds

*Click a project to expand — architecture notes and stack are inside.*

<details>
<summary><b>⚡ realtime-retail-analytics-pipeline</b> — streaming fraud detection on Kafka</summary>
<br/>

Kafka-based streaming pipeline with 60-second tumbling-window aggregation and rolling z-score anomaly detection, landing into Postgres with a Streamlit dashboard on top.

`Kafka` · `Python` · `PostgreSQL` · `Docker` · `Streamlit`

**[→ View repository](https://github.com/Satyammedya33/realtime-retail-analytics-pipeline)**
</details>

<details>
<summary><b>🏭 airflow-elt-warehouse-pipeline</b> — orchestrated ELT into a star-schema warehouse</summary>
<br/>

Airflow-orchestrated ELT with dbt-style SQL models feeding a star-schema warehouse, gated end-to-end by automated data-quality checks.

`Airflow` · `SQL` · `Data Quality` · `CI`

**[→ View repository](https://github.com/Satyammedya33/airflow-elt-warehouse-pipeline)**
</details>

<details>
<summary><b>🏞️ aws-data-lakehouse-pipeline</b> — medallion lakehouse on AWS</summary>
<br/>

Bronze / Silver / Gold medallion architecture on S3, provisioned with Terraform, queried Athena-style through DuckDB.

`AWS S3` · `Terraform` · `Parquet` · `DuckDB`

**[→ View repository](https://github.com/Satyammedya33/aws-data-lakehouse-pipeline)**
</details>

<details>
<summary><b>🛡️ llm-redteam-safety-framework</b> — probing LLMs for prompt-injection resistance</summary>
<br/>

A defensive probe suite that scores how well an LLM resists prompt injection and jailbreak attempts, using canary-token scoring for objective pass/fail results.

`AI Security` · `Python` · `Eval Harness`

**[→ View repository](https://github.com/Satyammedya33/llm-redteam-safety-framework)**
</details>

<details>
<summary><b>🔒 ml-network-intrusion-detection</b> — classifying network attacks</summary>
<br/>

Random Forest / XGBoost classifiers detecting DoS, Probe, and R2L network attacks, wrapped in a Streamlit triage dashboard for analysts.

`scikit-learn` · `XGBoost` · `Streamlit`

**[→ View repository](https://github.com/Satyammedya33/ml-network-intrusion-detection)**
</details>

<sub>Every repo above ships with a working Docker/CI setup, a test suite, and a README with an architecture diagram — click through, don't take my word for it.</sub>

<br/>

## 🧰 Tech stack

<table>
<tr><td valign="top" width="50%">

**Languages**
<br/>
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/-SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white)
![Java](https://img.shields.io/badge/-Java-007396?style=flat-square&logo=openjdk&logoColor=white)
![C++](https://img.shields.io/badge/-C%2B%2B-00599C?style=flat-square&logo=cplusplus&logoColor=white)

**Data engineering**
<br/>
![Kafka](https://img.shields.io/badge/-Apache%20Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white)
![Airflow](https://img.shields.io/badge/-Apache%20Airflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white)
![Postgres](https://img.shields.io/badge/-PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![AWS](https://img.shields.io/badge/-AWS-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/-Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![DuckDB](https://img.shields.io/badge/-DuckDB-FFF000?style=flat-square&logo=duckdb&logoColor=black)

</td><td valign="top" width="50%">

**ML / AI / security**
<br/>
![scikit-learn](https://img.shields.io/badge/-scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/-XGBoost-2C8EBB?style=flat-square)
![TensorFlow](https://img.shields.io/badge/-TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/-NumPy-013243?style=flat-square&logo=numpy&logoColor=white)

**Tools**
<br/>
![Git](https://img.shields.io/badge/-Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Power BI](https://img.shields.io/badge/-Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Jupyter](https://img.shields.io/badge/-Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)

</td></tr>
</table>

<br/>

## 📊 GitHub analytics

<div align="center">
<img height="165" src="https://github-readme-stats.vercel.app/api?username=Satyammedya33&show_icons=true&theme=tokyonight&hide_border=true&count_private=true" />
<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Satyammedya33&layout=compact&theme=tokyonight&hide_border=true" />
</div>

<div align="center">
<img src="https://github-readme-streak-stats.herokuapp.com/?user=Satyammedya33&theme=tokyonight&hide_border=true" />
</div>

<div align="center">
<img src="https://github-profile-trophy.vercel.app/?username=Satyammedya33&theme=tokyonight&no-frame=true&row=1&column=6&margin-w=8" />
</div>

<br/>

## 🐍 Contribution graph

<div align="center">
<img src="https://raw.githubusercontent.com/Satyammedya33/Satyammedya33/output/github-contribution-grid-snake-dark.svg" alt="contribution snake animation" width="100%" />
</div>

<sub>Generated by the workflow in <code>.github/workflows/snake.yml</code> — see the setup note below to switch it on.</sub>

<br/>

## 🤝 Let's connect

<div align="center">

| | |
|---|---|
| 📧 Email | [satyam.mdya33@gmail.com](mailto:satyam.mdya33@gmail.com) |
| 💼 LinkedIn | [satyam-medya](https://www.linkedin.com/in/satyam-medya-2b2825370) |
| 💬 Talk to me about | pipelines, data quality, or AI security |

</div>

<div align="center">
<sub>Thanks for stopping by — this README is generated and interactive, click around ⬆️</sub>
</div>
