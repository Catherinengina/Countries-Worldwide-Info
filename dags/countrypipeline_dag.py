from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add pipeline directory to path for Docker
pipeline_dir = '/opt/airflow/pipeline'
if not os.path.exists(pipeline_dir):
    raise FileNotFoundError(f"Pipeline directory not found: {pipeline_dir}")
sys.path.insert(0, pipeline_dir)

try:
    from countrypipeline_script import run_pipeline
except ImportError as e:
    raise ImportError(f"Failed to import run_pipeline: {e}")

# DAG default arguments
default_args = {
    'owner': 'catherine',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 8),
    'email': ['nginakate85@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
with DAG(
    'countries_pipeline',
    default_args=default_args,
    description='ETL pipeline for countries data',
    schedule_interval='@daily',
    catchup=False
) as dag:
    task_run_pipeline = PythonOperator(
        task_id='run_pipeline_task',
        python_callable=run_pipeline,
    )