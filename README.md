# Getting started

- [Install Airflow](#create-service)
- [Add a plugin](#add-a-plugin)
- [Watch the Infrastracture](#watch-the-infrastracture)
  - [Distribution List](#distribution-list)
  - [Tree view](#tree-view)

## Install Airflow

Follow after the [Quick Start](https://airflow.apache.org/docs/apache-airflow/2.0.1/start/docker.html) or the below steps:

#### Step 1

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.0.1/docker-compose.yaml
```

#### Step 2

```bash
mkdir ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

#### Step 3

```bash
docker-compose up airflow-init
```

#### Step 4

Edit the docker-compose.yaml and change the image to 1.10.13 (That's what we use in NI)

```bash
image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:1.10.13-python3.6}
```

#### Step 5

Define the plugin folder to be under the DAGs folder.
We defined it under DAGs folder because our EFS mounts the DAGs and we want to keep having the plugins folder while Airflow got restarted

```bash
AIRFLOW__CORE__PLUGINS_FOLDER: '/opt/airflow/dags/plugins'
```

#### Step 6

```bash
docker-compose up -d
```

## Add the plugin

Place the plugin folder in the dags folder

```bash
cp plugins dags/
```

Restart Airflow web and scheduler

```bash
docker container restart airflow_airflow-scheduler_1 && docker container restart airflow_airflow-webserver_1
```

## Watch the Infrastracture

##### Distribution List

Watch the [distribution list](http://localhost:8080/admin/distribution/)

##### Tree view

Watch the [tree view](http://localhost:8080/admin/dags/)

