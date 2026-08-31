from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

default_args = {
    'owner': 'mezba',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'netflix_etl_pipeline',
    default_args=default_args,
    description='Bronze->Silver->Gold Netflix ETL',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2026, 8, 31),
    catchup=False,
    tags=['netflix', 'etl'],
) as dag:

    def extract_task():
        from extract import load_csv_to_postgres, verify
        load_csv_to_postgres(r"C:\Users\Lenovo\Desktop\data-engineering-journey\netflix_titles.csv")
        verify()

    def transform_task():
        from transform import read_bronze, clean_data, load_silver, validate_silver
        df = read_bronze()
        clean = clean_data(df)
        load_silver(clean)
        validate_silver()

    def load_task():
        from star_schema import build_dimensions
        from fact_loader import build_fact_table, verify_star_schema
        build_dimensions()
        build_fact_table()
        verify_star_schema()

    t1 = PythonOperator(task_id='extract', python_callable=extract_task)
    t2 = PythonOperator(task_id='transform', python_callable=transform_task)
    t3 = PythonOperator(task_id='load', python_callable=load_task)

    t1 >> t2 >> t3

