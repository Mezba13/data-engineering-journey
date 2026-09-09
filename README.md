# Data Engineering Journey

A hands-on Data Engineering learning journey covering Python, SQL, PostgreSQL, Docker, ETL pipelines, data modeling, and dbt.

This repository contains both my **learning exercises** and my **portfolio project**, showing how I progressed from individual data engineering concepts to building an end-to-end data pipeline.

---

## 🚀 Featured Project

### Netflix Data Pipeline

The main portfolio project in this repository is an end-to-end Netflix data pipeline built using:

* Python
* Pandas
* SQLAlchemy
* PostgreSQL
* Docker
* dbt
* Git

The pipeline takes Netflix title data from a CSV file, performs extraction and transformation, loads the data into PostgreSQL, and uses dbt for further transformation, testing, documentation, snapshots, and reusable SQL logic.

---

## 🏗️ Architecture

```text
                    Netflix Data Pipeline

┌─────────────────────┐
│ netflix_titles.csv  │
│      Raw Data       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Python ETL      │
│                     │
│ Extract              │
│ Transform            │
│ Load                 │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     PostgreSQL      │
│                     │
│ Bronze: netflix     │
│ Silver: clean_silver│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│        dbt          │
│                     │
│ Staging Models      │
│ Mart Models         │
│ Tests               │
│ Snapshots           │
│ Macros              │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Analytics Models    │
│                     │
│ dim_content_type    │
│ fct_title_metrics   │
└─────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose                                                  |
| ---------- | -------------------------------------------------------- |
| Python     | Data extraction, transformation and loading              |
| Pandas     | Data cleaning and transformation                         |
| SQLAlchemy | Python-to-PostgreSQL database connection                 |
| PostgreSQL | Relational database / data warehouse                     |
| Docker     | Containerized PostgreSQL environment                     |
| dbt        | SQL transformation, testing, documentation and snapshots |
| Git        | Version control                                          |
| PowerShell | Local development and automation                         |

---

## 📁 Repository Structure

```text
data-engineering-journey/
│
├── README.md
│
├── netflix-data-pipeline/
│   │
│   ├── python-pipeline/
│   │   ├── main.py
│   │   └── src/
│   │       ├── __init__.py
│   │       ├── dimensions.py
│   │       ├── extract.py
│   │       ├── facts.py
│   │       └── transform.py
│   │
│   ├── dbt/
│   │   └── dbt_netflix/
│   │       ├── dbt_project.yml
│   │       ├── models/
│   │       │   ├── schema.yml
│   │       │   ├── sources.yml
│   │       │   ├── staging/
│   │       │   │   └── stg_netflix.sql
│   │       │   └── marts/
│   │       │       ├── dim_content_type.sql
│   │       │       └── fct_title_metrics.sql
│   │       ├── snapshots/
│   │       │   └── snapshot_netflix.sql
│   │       └── macros/
│   │           └── content_category.sql
│   │
│   ├── sql/
│   │   └── queries_silver.sql
│   │
│   └── images/
│
├── week1-day1/
├── week1-day2/
├── week1-day3/
├── week1-day5/
├── week1-day6/
├── week2-day8/
├── week2-day10/
├── movie-pipeline/
├── dbt_netflix/
└── other learning materials...
```

The `week1-day*` and `week2-day*` folders are intentionally preserved as part of my learning history.

---

## 🔄 Python ETL Pipeline

The Python pipeline is organized into separate modules:

### `extract.py`

Responsible for extracting/loading the raw Netflix dataset into PostgreSQL.

### `transform.py`

Responsible for cleaning and transforming the raw data.

### `dimensions.py`

Creates and loads dimension tables for the analytical data model.

### `facts.py`

Creates and loads fact data for analytical use.

### `main.py`

Acts as the pipeline entry point and coordinates the different stages.

The overall flow is:

```text
CSV
 ↓
Extract
 ↓
Bronze: netflix
 ↓
Transform
 ↓
Silver: clean_silver
 ↓
Dimensions / Facts
```

---

## 🧱 Bronze-Silver-Gold Architecture

### Bronze

Raw data loaded from the Netflix CSV:

```text
netflix
```

### Silver

Cleaned and transformed data:

```text
clean_silver
```

### Gold / Analytics

Analytical models are created from the cleaned data using Python and dbt.

The dbt layer currently contains:

```text
dim_content_type
fct_title_metrics
```

---

## 📊 dbt

The dbt project is located at:

```text
netflix-data-pipeline/dbt/dbt_netflix/
```

### Staging

```text
stg_netflix
```

The staging model reads from the PostgreSQL `clean_silver` table using a dbt source.

```sql
{{ source('netflix_pipeline', 'clean_silver') }}
```

### Mart Models

```text
dim_content_type
fct_title_metrics
```

dbt models use `ref()` to create dependencies between models.

Example:

```sql
{{ ref('stg_netflix') }}
```

---

## ✅ Data Quality Testing

The dbt project includes tests such as:

* `not_null`
* `unique`
* `accepted_values`

For example, the Netflix `type` column is tested to contain only:

```text
Movie
TV Show
```

The pipeline currently has seven configured dbt data tests, all passing.

---

## 🕐 dbt Snapshots

The project uses dbt snapshots to track historical changes in Netflix records.

The snapshot monitors fields such as:

* rating
* duration
* listed_in

using:

```text
show_id
```

as the unique key.

This provides a history of changes rather than only keeping the current version of a record.

---

## ♻️ dbt Macros

Reusable SQL logic is implemented using dbt macros.

For example, the project contains a macro that categorizes Netflix content:

```text
Movie    → Film Content
TV Show  → Series Content
```

The macro demonstrates how reusable SQL logic can be written once and used across multiple models.

---

## ▶️ How to Run

### 1. Start PostgreSQL

Make sure the PostgreSQL Docker container is running:

```powershell
docker ps
```

If the container already exists but is stopped:

```powershell
docker start postgres-de
```

---

### 2. Run the Python Pipeline

```powershell
cd C:\Users\Lenovo\desktop\data-engineering-journey\netflix-data-pipeline\python-pipeline

python main.py
```

This runs the Python ETL pipeline.

---

### 3. Run dbt

Move into the dbt project:

```powershell
cd C:\Users\Lenovo\desktop\data-engineering-journey\netflix-data-pipeline\dbt\dbt_netflix
```

Run the models:

```powershell
dbt run
```

Run the tests:

```powershell
dbt test
```

Generate documentation:

```powershell
dbt docs generate
```

Start the documentation server:

```powershell
dbt docs serve --port 8081
```

---

## 🔍 Useful PostgreSQL Commands

Connect to the database through Docker:

```powershell
docker exec -it postgres-de psql -U postgres -d netflix_db
```

Inside PostgreSQL:

```sql
\dt
```

List tables.

```sql
\dv
```

List views.

```sql
\dn
```

List schemas.

Exit PostgreSQL:

```sql
\q
```

---

## 📈 Example Analytics Query

Example: finding the most common countries among Netflix titles.

```sql
SELECT
    country,
    COUNT(*) AS title_count
FROM clean_silver
WHERE country IS NOT NULL
GROUP BY country
ORDER BY title_count DESC
LIMIT 10;
```

---

## 🎯 Key Learning Areas

Through this project, I have practiced:

* Python programming
* Pandas
* Data cleaning
* CSV processing
* ETL pipeline design
* PostgreSQL
* SQL
* SQLAlchemy
* Docker
* Database connectivity
* Data modeling
* Dimension and fact tables
* dbt models
* dbt `ref()`
* dbt `source()`
* dbt tests
* dbt snapshots
* dbt macros
* Data lineage
* Git and GitHub
* Project organization

---

## 📚 Learning Journey

The learning folders are intentionally preserved.

They represent the progression from individual exercises and experiments to a complete end-to-end data engineering project.

```text
Learning Exercises
       ↓
Python & Pandas
       ↓
SQL
       ↓
PostgreSQL
       ↓
Docker
       ↓
ETL
       ↓
Data Modeling
       ↓
dbt
       ↓
End-to-End Pipeline
       ↓
Portfolio Project
```

---

## 👨‍💻 Author

**Mezba Uddin Moyur**

Aspiring Data Engineer

Currently working as an Assistant Teacher, ICT, while building practical skills and projects in Data Engineering.

---

## 🚧 Future Improvements

Planned improvements may include:

* Cloud data warehouse integration
* Airflow orchestration
* Automated pipeline scheduling
* CI/CD
* More analytical dbt models
* Advanced data quality tests
* Incremental models
* Data visualization
* Cloud deployment
* Production-style monitoring
