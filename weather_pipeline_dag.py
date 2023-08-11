import json
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


# Python functions
def download_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8534&longitude=2.3488&hourly=temperature_2m&timezone=auto&format=json"
    response = requests.get(url)
    data = response.json()
    with open("./weather_data.json", "w") as file:
        json.dump(data, file, indent=2)


def transform_data():
    df = pd.read_json("./weather_data.json", orient="index")[0]
    date = sorted({dt.split("T")[0] for dt in df["hourly"]["time"]})
    df_date = pd.to_datetime(date)
    temperatures = df["hourly"]["temperature_2m"]
    avg_temp = [
        np.mean(temperatures[i : i + 24]) for i in range(0, len(temperatures), 24)
    ]
    print(df_date)
    df["avg_temperature"] = {
        "date": df_date.strftime("%Y-%m-%d"),
        "temperature": avg_temp,
    }
    df.to_json("./transformed_data.json", indent=2)


# Default arguments for the DAG
default_args = {
    "owner": "admin",
    "depends_on_past": False,
    "start_date": datetime(2023, 8, 11),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# Create a DAG instance
dag = DAG(
    "weather_pipeline",
    default_args=default_args,
    description="DAG to automate the data processing",
    schedule_interval=timedelta(hours=1),
)

# Define the tasks

# Task 1:
download_task = PythonOperator(
    task_id="download_weather_data",
    python_callable=download_weather_data,
    dag=dag,
)

## Task 2:
transform_task = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    dag=dag,
)

# Set the task dependencies
download_task >> transform_task
