# Automated Weather Data Pipeline
This small project focuses on the use of Apache Airflow to learn more on data pipeline orchestration.

Help from https://airflow.apache.org/.

## Overview
This project involves building an automated data pipeline using Apache Airflow to download weather data, calculate average temperatures, and store the results.

## Steps followed

### 0. Installation & Setup
```bash
# Install Apache Airflow
pip install apache-airflow

# Modify the AIRFLOW_HOME in the project directory
export AIRFLOW_HOME=$(pwd)/airflow

# Initialize the Airflow database at $AIRFLOW_HOME
airflow db init

# If it's the first time, we must set an user
airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin

# Start the Airflow web server and scheduler (in two terminals)
airflow webserver -p 8080
airflow scheduler
```

### 1. Modify the config file for the Apache Airflow webserver
When the initialization of the Airflow database done, we can access to the config file. Inside we can check the default configuration.

Changes made:
```python
load_examples = False
default_timezone = Europe/Paris
expose_config = True
dags_are_paused_at_creation = False
```

### 2. Create DAG (Directed Acyclic Graph)
For the dataset, I retrieved data from the following website https://open-meteo.com/ (for more details, go check the [docs](https://open-meteo.com/en/docs)).

```python
# Default arguments for the DAG
# ...

# Create a DAG instance
# ...
```

### 3. Write Python functions for the tasks

```python
# Download the weather data
# ...

# Transform and save new data
# ...
```

### 4. Create Airflow tasks and define task operators
As the code is written in Python, the `PythonOperator` library is used to create the tasks. Once the operators are set, they must be defined in order, so with `>>` operator.

```python
# For instance the task_1 is executed, then task_2 and task_3 are executed, finally it ends with task_4
task_1 >> [task_2, task_3] >> task_4
```

For more details on tasks, go check the [docs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html).

### 5. Move the DAG Python file into the right folder
Basically, by default, DAGs are located in `$AIRFLOW_HOME/dags` directory. So the `weather_pipeline_dag.py` must be inside this folder.

```bash
mkdir $AIRFLOW_HOME/dags
mv weather_pipeline_dag.py $AIRFLOW_HOME/dags
```

### Where I got a bit stuck / Interesting points
- To check the list of DAGs, we can run `airflow dags list`.
- If there's a problem with DAGs, the command `airflow dags list-import-errors` provides the errors encountered.
- The timezone must be checked carefully. It may causes some problems, especially for the run of DAGs, it won't run automatically for instance.

### Extra: Setup of pre-commit
```bash
pip install pre-commit
```

Once the `.pre-commit-config.yaml` completed, we need to set up the git hooks scripts.

```bash
pre-commit install
```