# Building Plotly Dash Apps on a Lakehouse with Databricks SQL

## Overview

Python developers who want to connect a Plotly Dash web app front end to a Databricks back end will be well-served by the Databricks SQL connector for Python, a specific form of the recently announced Databricks SQL capability.

This library allows Plotly Dash apps to very quickly run AND retrieve results of SQL queries that are executed on a Databricks cluster, thus allowing Databricks customers to extend their use of Databricks:

- For any/all manner of data warehousing use case
- With an ORM (e.g. SQLAlchemy) to perform advanced use cases such as:
    - Waterfall filtering/visualizations
    - Sliders/filters/dependent visuals
    - Periodic updates for streaming dashboards
    - Pushing expensive SQL transformations to the Databricks SQL Photon engine
- To simplify back-end architectures and costs to accommodate use cases such as the above (e.g. avoiding external caching architecture work-arounds)
- To allow Databricks users (highly technical BI engineers, data scientists, data engineers) to easily develop simple through to sophisticated interactive data analytics and visualization web application experiences for which Dash is highly differentiated.

As described in the Databricks technical integration document linked above, most of the environment variables used in the code snippets (see utils folder) can be found in the "Advanced Options > JDBC/ODBC" tab of your Databricks cluster.

In this first of three examples, data is returned as a PyArrow table, which can be well-suited for retrieving large volumes of data. [NOTE: If necessary, this table can be converted to other formats, such as Pandas dataframes, Numpy arrays, or VAEX dataframes (also used for larger data volume workflows)].

This data can then be consumed by Dash open-source components (including Plotly graphs) along with Dash Enterprise licensed capabilities (including Plotly’s DashBoard Engine) following a standard approach.

NB: This app is deployed [here](https://dash-services.plotly.host/dash-dbx-sql/).

## Development

### DBX backend

1. Spin up a DatabricksSQL (DBSQL) Endpoint on either Classic or Serverless
2. Copy and paste the SQL code under `utils/BuildBackendIoTDatabase.sql`  into the DBSQL Query Editor and run it. You can also run this code in a notebook directly from an imported Repo in Databricks. This will populate the database required for this app.

### Dash frontend

1. Clone this repo into your local IDE

```
git clone https://github.com/plotly/dash-dbx-sql.git
```

2. Create a virtual Python environment (eg. `venv` or `conda`) and install the dependencies

```
pip install -r requirements.txt
```

3. Set environment variables of `HOST_NAME`, `HTTP_PATH`, `ACCESS_TOKEN` from your Databricks cluster. You can find this by selecting the SQL endpoint and clicking the [“Connection Details” tab in the Endpoint UI](https://docs.databricks.com/sql/admin/sql-endpoints.html#view-sql-endpoints). You can also put these in a `.env` file in your top-level project directory. 

4. Start up a local development server by running

```
python app.py
```

