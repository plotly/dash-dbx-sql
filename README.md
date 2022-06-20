# dash-dbx-sql

Python developers who want to connect a Plotly Dash web app front end to a Databricks back end will be well-served by the Databricks SQL connector for Python, a specific form of the recently announced Databricks SQL capability.

This library allows Plotly Dash apps to very quickly run AND retrieve results of SQL queries that are executed on a Databricks cluster, thus allowing Databricks customers to extend their use of Databricks:

- for any/all manner of data warehousing use case
- with an ORM (e.g. SQLAlchemy) to perform advanced use cases such as:
- waterfall filtering/visualizations
- sliders/filters/dependent visuals
- period updates for streaming dashboards
- pushing expensive SQL transformations to the Databricks SQL Photon engine
- to simplify back-end architectures and costs to accommodate use cases such as the above (e.g. avoiding external caching architecture work-arounds)
- to allow Databricks users (highly technical BI engineers, data scientists, data engineers) to easily develop simple through to sophisticated interactive data analytics and visualization web application experiences for which Dash is highly differentiated.
As described in the Databricks technical integration document linked above, most of the environment variables used in the code snippets below can be found in the "Advanced Options > JDBC/ODBC" tab of your Databricks cluster.

In this first of three examples (see utils folder), data is returned as a PyArrow table, which can be well-suited for retrieving large volumes of data. [NOTE: If necessary, this table can be converted to other formats, such as Pandas dataframes, Numpy arrays, or VAEX dataframes (also used for larger data volume workflows)].

This data can then be consumed by Dash open-source components (including Plotly graphs) along with Dash Enterprise licensed capabilities (including Plotly’s DashBoard Engine) following a standard approach.
