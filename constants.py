import os
from dotenv import load_dotenv

load_dotenv()  # loads environment variables from .env file

## Database
DB_NAME = "plotly_iot_dashboard"
USER_TABLE = "silver_users"
DEVICE_TABLE = "silver_sensors"

SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
HTTP_PATH = os.getenv("HTTP_PATH")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

## Other

app_description = {
    "headers": [
        "Databricks as a Data Warehouse",
        "Fast Query, Computation, & Retrieval of Databricks Data",
        "Gateway to Sophisticated Data Science",
    ],
    "texts": [
        "for simple to advanced python analytical workflows",
        "at scale via Plotly Dash analytical web applications",
        "for simple to advanced python analytical workflows",
    ],
}
demographics_data_dict = {
    "headers": ["Data Source", "Data Acquisition", "Query"],
    "texts": [
        "'silver_users' table inside Serverless Databricks SQL database",
        "Every time user interacts with the filters on the page, Dash talks to the database",
        "This query COUNTS results from a GROUP BY query, which depending on filters looks can group by height, sex, and risk",
    ],
}

fitness_data_dict = {
    "headers": ["Data Source", "Query"],
    "texts": [
        "'silver_users' and 'silver_sensors' tables which hold user and wearable devices information respectively",
        "JOIN the two tables on the user_id column. This query pulls the data for a user-specified fitness metric, averaged by specified demographic group broken down BY comparison category, per day",
    ],
}

heatmap_data_dict = {
    "headers": ["Data Source", "Query"],
    "texts": [
        "'silver_users' and 'silver_sensors' tables",
        "JOIN the two tables on the user_id column. This query pulls the data WHERE it filters by user-specified comparison categories, BETWEEN performance percentile, and then averages the result for each demographic group",
    ],
}


custom_color = {
    "sex": ["#DB4C39", "#39c8db"],
    "Smoker": ["rgb(0, 0, 0)", "#DB4C39"],
    "cholesterol": ["rgb(48, 255, 69)", "rgb(252, 50, 50)"],
    "bloodpressure": ["rgb(252, 50, 50)", "rgb(48, 255, 69)"],
}
