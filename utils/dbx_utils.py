from constants import (
    SERVER_HOSTNAME,
    HTTP_PATH,
    ACCESS_TOKEN,
    DB_NAME,
    USER_TABLE,
    DEVICE_TABLE,
)
from databricks import sql


def get_user_data(user, fitness):
    """
    Fetches user data for a specific user id from silver_users table, returns it as a pandas dataframe

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
        f"""SELECT *
            FROM(
                SELECT
                CASE WHEN gender='F' THEN 'Female' ELSE 'Male' END AS sex, 
                CASE WHEN smoker='N' THEN 'Non-smoker' ELSE 'Smoker' END AS Smoker,
                cholestlevs AS cholesterol, bp AS bloodpressure, userid,
                age, height, weight
                FROM {DB_NAME}.{USER_TABLE}
            )
            WHERE userid = {user}
            """
    )
    userdemodf = cursor.fetchall_arrow()
    userdemodf = userdemodf.to_pandas()
    cursor.close()
    cursor = connection.cursor()
    cursor.execute(
        f"""SELECT date, SUM({fitness}) AS {fitness}
            FROM(
                SELECT
                CAST({DEVICE_TABLE}.timestamp AS DATE) AS date,
                num_steps*0.00035 AS num_steps, miles_walked*0.0003 AS miles_walked, calories_burnt*0.002 AS calories_burnt
                FROM {DB_NAME}.{DEVICE_TABLE}
                WHERE user_id = {user}
            )
            GROUP BY date
            ORDER BY date
            """
    )
    userfitdf = cursor.fetchall_arrow()
    userfitdf = userfitdf.to_pandas()
    cursor.close()
    connection.close()
    return userdemodf, userfitdf


def get_scatter_data(xaxis, comp):
    """
    Fetches specified columns and an aggregated column from the silver_users table, returns it as a pandas dataframe

    Returns
    -------
    df : pandas dataframe
        basic query of data from Databricks as a pandas dataframe
    """
    connection0 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor0 = connection0.cursor()
    cursor0.execute(
        f"""SELECT {xaxis}, {comp}, risk, Count(DISTINCT userid) AS Total 
            FROM(
                SELECT
                CASE WHEN gender='F' THEN 'Female' ELSE 'Male' END AS sex,
                age, height, weight, 
                CASE WHEN smoker='N' THEN 'Non-smoker' ELSE 'Smoker' END AS Smoker,
                cholestlevs AS cholesterol, bp AS bloodpressure, risk, userid
                FROM {DB_NAME}.{USER_TABLE}
            )
            GROUP BY {xaxis}, {comp}, risk
            """
    )
    df = cursor0.fetchall_arrow()
    df = df.to_pandas()
    cursor0.close()
    connection0.close()
    return df


def get_line_data(yaxis, comp):
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
                cholestlevs AS cholesterol, bp AS bloodpressure, user_id,
                SUM(num_steps*0.00035) AS num_steps, SUM(miles_walked*0.0003) AS miles_walked, SUM(calories_burnt*0.002) AS calories_burnt
                FROM {DB_NAME}.{DEVICE_TABLE}
                LEFT JOIN {DB_NAME}.{USER_TABLE} ON {DEVICE_TABLE}.user_id = {USER_TABLE}.userid
                GROUP BY sex, Smoker, date, user_id, cholesterol, bloodpressure
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
                SUM(num_steps*0.00035) AS num_steps, SUM(miles_walked*0.0003) AS miles_walked, SUM(calories_burnt*0.002) AS calories_burnt,
                age, height, weight, user_id
                FROM {DB_NAME}.{DEVICE_TABLE}
                LEFT JOIN {DB_NAME}.{USER_TABLE} ON {DEVICE_TABLE}.user_id = {USER_TABLE}.userid
                WHERE {fitness} BETWEEN ((SELECT MAX({fitness}) FROM {DB_NAME}.{DEVICE_TABLE})*{slider[0]}*0.01) 
                AND ((SELECT MAX({fitness}) FROM {DB_NAME}.{DEVICE_TABLE})*{slider[1]}*0.01)
                GROUP BY sex, Smoker, cholesterol, bloodpressure, user_id, age, height, weight
            )
            GROUP BY {comp}, {axis1}, {axis2}
            """
    )
    df = cursor2.fetchall_arrow()
    df = df.to_pandas()
    cursor2.close()
    connection2.close()
    return df


def get_listofusers(dash_prepare=False):
    connection3 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor3 = connection3.cursor()
    cursor3.execute(
        f"SELECT DISTINCT userid FROM {DB_NAME}.{USER_TABLE} ORDER BY userid ASC"
    )
    df = cursor3.fetchall_arrow()
    df = df.to_pandas()
    cursor3.close()
    connection3.close()
    if dash_prepare:
        return [{"label": str(i), "value": str(i)} for i in df["userid"]]
    return df


def get_user_comp(fitness):
    connection4 = sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    )
    cursor4 = connection4.cursor()
    cursor4.execute(
        f"""SELECT user_id, {fitness}
            FROM(
                SELECT
                SUM(num_steps*0.00035) AS num_steps, SUM(miles_walked*0.0003) AS miles_walked, SUM(calories_burnt*0.002) AS calories_burnt,
                user_id
                FROM {DB_NAME}.{DEVICE_TABLE}
                LEFT JOIN {DB_NAME}.{USER_TABLE} ON {DEVICE_TABLE}.user_id = {USER_TABLE}.userid 
                GROUP BY user_id
            )
            ORDER BY {fitness} ASC
            """
    )
    df = cursor4.fetchall_arrow()
    df = df.to_pandas()
    cursor4.close()
    connection4.close()
    return df
