from databricks import sql
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd

load_dotenv()

SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
HTTP_PATH = os.getenv("HTTP_PATH")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

DB_NAME = "plotly_iot_dashboard"
USER_TABLE = "silver_users"
DEVICE_TABLE = "silver_sensors"


def get_user_data(xaxis, comp):
    """
    Fetches specified columns and an aggregated column from the silver_users table, returns it as a pandas dataframe

    Returns
    -------
    df : pandas dataframe
        basic query of data from Databricks as a pandas dataframe
    """
    connection = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor = connection.cursor()
    cursor.execute(
        f"""SELECT {xaxis}, {comp}, risk, Count(*) AS Total 
            FROM(
                SELECT
                CASE WHEN gender='F' THEN 'Female' ELSE 'Male' END AS sex,
                age, height, weight, 
                CASE WHEN smoker='N' THEN 'Non-smoker' ELSE 'Smoker' END AS Smoker,
                cholestlevs AS cholesterol, bp AS bloodpressure, risk
                FROM {DB_NAME}.{USER_TABLE}
            )
            GROUP BY {xaxis}, {comp}, risk
            """
    )
    df = cursor.fetchall_arrow()
    df = df.to_pandas()
    cursor.close()
    connection.close()
    return df


def join_user_sensor(yaxis, comp):
    """
    Joins the user and sensor tables, selects specified columns and an aggregated column, returns it as a pandas dataframe

    Returns
    -------
    df : pandas dataframe
        basic query of data from Databricks as a pandas dataframe
    """
    connection1 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor1 = connection1.cursor()
    cursor1.execute(
        f"""SELECT date, {comp}, AVG({yaxis}) AS {yaxis}tot 
            FROM(
                SELECT
                CASE WHEN gender='F' THEN 'Female' ELSE 'Male' END AS sex, 
                CASE WHEN smoker='N' THEN 'Non-smoker' ELSE 'Smoker' END AS Smoker,
                CAST({DEVICE_TABLE}.timestamp AS DATE) AS date,
                cholestlevs AS cholesterol, bp AS bloodpressure,
                num_steps, miles_walked, calories_burnt
                FROM {DB_NAME}.{DEVICE_TABLE}
                LEFT JOIN {DB_NAME}.{USER_TABLE} ON {DEVICE_TABLE}.user_id = {USER_TABLE}.userid
            )
            GROUP BY date, {comp}
            ORDER BY date
            """
    )
    df = cursor1.fetchall_arrow()
    df = df.to_pandas()
    cursor1.close()
    connection1.close()
    return df


def get_heat_data(axis1, axis2, fitness, comp, slider):
    """
    Fetches data from the Databricks database and returns it as a pandas dataframe

    Returns
    -------
    df : pandas dataframe
        basic query of data from Databricks as a pandas dataframe
    """
    connection2 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor2 = connection2.cursor()
    cursor2.execute(
        f"""SELECT {axis1}, {axis2}, {comp}, AVG({fitness}) AS {fitness}tot 
            FROM(
                SELECT
                CASE WHEN gender='F' THEN 'Female' ELSE 'Male' END AS sex, 
                CASE WHEN smoker='N' THEN 'Non-smoker' ELSE 'Smoker' END AS Smoker,
                cholestlevs AS cholesterol, bp AS bloodpressure,
                num_steps, miles_walked, calories_burnt, age, height, weight
                FROM {DB_NAME}.{DEVICE_TABLE}
                LEFT JOIN {DB_NAME}.{USER_TABLE} ON {DEVICE_TABLE}.user_id = {USER_TABLE}.userid
                WHERE {fitness} BETWEEN ((SELECT MAX({fitness}) FROM {DB_NAME}.{DEVICE_TABLE})*{slider[0]}*0.01) 
                AND ((SELECT MAX({fitness}) FROM {DB_NAME}.{DEVICE_TABLE})*{slider[1]}*0.01)
            )
            GROUP BY {comp}, {axis1}, {axis2}
            """
    )
    df = cursor2.fetchall_arrow()
    df = df.to_pandas()
    cursor2.close()
    connection2.close()
    return df
