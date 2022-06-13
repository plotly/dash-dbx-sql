# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC # These are the connectors we need to install

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC pip install dash
# MAGIC pip install sqlalchemy
# MAGIC pip install sqlalchemy-databricks

# COMMAND ----------

# DBTITLE 1,Imports/Configs
from dash import Dash
from dash import dcc
from dash import html, Input, Output
import flask
import json
import pandas as pd
from sqlalchemy import *
from sqlalchemy.engine import create_engine
import plotly.express as px
import re

## Waterfall
## Streaming example - Dash updates in real time at intervals

### Set up Configs
with open('config.json') as w:

    conf = json.load(w)
    token = conf.get("token")
    http_path = conf.get("http_path")
    database = conf.get("database")
    host_name = conf.get("host_name")

### Initialize Database Connection

engine = create_engine(
    f"databricks+connector://token:{token}@{host_name}:443/{database}",
    connect_args={
        "http_path": http_path,
    },  
    )

print(f"Loading from DBX Server: {host_name} on database: {database}")

# COMMAND ----------

# DBTITLE 1,App Code

### Core Dash App

app = Dash(__name__)

app.layout = html.Div([
        html.Label("Choose your Sensor Measurement: "),
        dcc.Dropdown(
            id='SensorDropdown',
            options = measurement_options, 
            multi=False),
        html.Br(),
        dcc.Graph(id='SensorOverTimeGraph')
    ])


@app.callback(
    Output(component_id="SensorOverTimeGraph", component_property="figure"),
    Input(component_id="SensorDropdown", component_property="value")
)
def update_graph(input_value):

    ## ORM-based SQL Query with dynamic filters in the callback
    stmt = select([
            sensor_table.columns.MeasurementDateTime,
            sensor_table.columns.LongMovingAverage,
            sensor_table.columns.SensorLocation
            ]).where(and_(
                sensor_table.columns.SensorMeasurement == input_value
            ))

    ## Read data via pandas or just raw Dict/array
    ## TIPS: Always try to push the filtering/complex logic down to the system where the most data is filtered
    ## minimize data brought to client
    df = pd.read_sql_query(stmt, engine).sort_values(by=['MeasurementDateTime'])

    fig_line = px.line(df, x="MeasurementDateTime",
                    y="LongMovingAverage",
                    color="SensorLocation",
                    title=f'Sensor Value Moving Averages Over Time for : {input_value}')



    ## Build Plot Figure and return

    return fig_line


# COMMAND ----------

if __name__ == '__main__':
    app.run_server(debug=True)
