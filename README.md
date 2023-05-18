# Image classification app, built with Databricks DB Connect "V2" and Dash

## Prerequisites

- [Local machine] JVM (I'm using JVM 11 in this example)
- [Local machine] [Poetry](https://python-poetry.org/)
- [Local machine] Databricks profile configured via [databricks-cli](https://docs.databricks.com/dev-tools/cli/index.html#set-up-authentication-using-a-databricks-personal-access-token)
- [Databricks] Databricks All-purpose Cluster with DBR 13.X or higher and UC enabled


## How-to

1. Install package and it's dependencies:

```bash
poetry install
```

2. Create a table with image metadata (check the possible arguments in the `conf/config.yaml` file):
```bash
poetry run frontend \
    --config-path="${PWD}/conf" \
    profile=some-databricks-profile \
    cluster_name=some-cluster-name
```

3. Run the app:
```bash
poetry run python \
    db_connect_v2_image_classification/frontend/app.py \
    --config-path="${PWD}/conf" \
    profile=some-databricks-profile \
    cluster_name=some-cluster-name
```

4. Open http://0.0.0.0:8050 and enjoy your app ✨

## Technologies used

- Databricks and DB Connect V2
- `hydra` for configuration management
- `poetry` for package management and project setup
- `black` for code formatting
- `ruff` for linting
- `isort` for import analysis
- Dash by Plotly as frontend framework
- Tailwind for CSS settings
- Daisy UI for some ready-to-use components