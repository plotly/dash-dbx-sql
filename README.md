# Building Plotly Dash Apps on a Lakehouse with Databricks SQL

Plotly on Databricks Blog Series — Article #1 (June/22)

## Authors 
Cody Austin Davis
 (Solutions Architect, Databricks), 
Hannah Ker
 (Solutions Architect, Plotly) 

   with special contributions from Daniel Anton Suchy & Tammy Do

## Links
[Medium Article](https://plotlygraphs.medium.com/b9761c201717)

[Plotly Dash App](https://dash-demo.plotly.host/dash-dbx-sql/)

[Youtube Video](https://www.youtube.com/watch?v=tmte0KqewD0)

# Overview

Python developers who want to connect a Plotly Dash web app front end to a Databricks back end will be well-served by the [Databricks SQL connector for Python](https://docs.databricks.com/dev-tools/python-sql-connector.html), a specific form of the recently announced Databricks SQL capability.

This library allows Plotly Dash apps to very quickly run AND retrieve results of SQL queries that are executed on a Databricks cluster, thus allowing Databricks customers to extend their use of Databricks:

- For any/all manner of data warehousing use case
- With an ORM (e.g. SQLAlchemy) to perform advanced use cases such as:
    - Waterfall filtering/visualizations
    - Sliders/filters/dependent visuals
    - Periodic updates for streaming dashboards
    - Pushing expensive SQL transformations to the Databricks SQL Photon engine
- To simplify back-end architectures and costs to accommodate use cases such as the above (e.g. avoiding external caching architecture work-arounds)
- To allow Databricks users (highly technical BI engineers, data scientists, data engineers) to easily develop simple through to sophisticated interactive data analytics and visualization web application experiences for which Dash is highly differentiated.

![Screen Shot 2022-06-24 at 2 23 16 PM](https://user-images.githubusercontent.com/48504233/175695446-511ebc34-e45b-4a6e-9cbb-ebf109428ddf.png)


For specific details of this integration, please refer to the Medium article at:

https://plotlygraphs.medium.com/b9761c201717
