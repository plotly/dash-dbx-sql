import os
from utils import dbx_utils
from dotenv import load_dotenv

load_dotenv() # loads environment variables from .env file

## Database
DB_NAME = "plotly_iot_dashboard"
USER_TABLE = "silver_users"
DEVICE_TABLE = "silver_sensors"

SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
HTTP_PATH = os.getenv("HTTP_PATH")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

## Other 

TEXT_DEMOGRAPHICS = """The data used for this graph comes from the silver_users table
which contains patient demographic data. A "group by" and "count" 
aggregation combo are implemented via SQL statement. The columns 
pulled into the Dash app are user-determined such that only data 
that is displayed is retrieved from SQL to improve latency. The 
"risk" column, the selected x-axis category column and the selected 
comparison category column are pulled and a calculated column counting 
the number of patients that fall into each unique combo of column 
values is also pulled. The calculation happens in Databricks and data 
is re-queried when the user changes either the x axis category or 
comparison category."""

TEXT_FITNESS_LINE = """The data used for this graph comes from the silver_users and 
silver_sensors tables. A join of the tables is done in SQL
wherein the sensor data is matched to the demographic data for 
that patient on the shared "user_id" column from each table.
The fitness metrics (number of steps, burned calories, miles walked) 
are reported by the sensors/devices for some date/time. A single SQL 
query is used to pull the data for a user-specified fitness metric, 
averaged by specified demographic group broken down by comparison 
category, per day."""

TEXT_HEAT_FIG = """The data used for this graph comes from the silver_users and 
silver_sensors tables. A join of the tables is done in SQL 
wherein the sensor data is matched to the demographic data for 
that patient on the shared "user_id" column from each table.
The fitness metrics (number of steps, burned calories, miles 
walked) are reported by the sensors/devices for some date/time. 
A single SQL query is used to pull the data for a user-specified 
fitness metric, averaged by specified demographic group over all 
days, broken down by comparison category. The graphs show the 
dependence of fitness metrics on the intersection of two demographic 
categories (x and y axis), one graph per comparison category. For 
example, when looking at age and height, the highest average calories 
burned per day by female patients is in the 40-44 year olds
with height between 55-59 inches whereas for male patients it's in the 
30-34 year old range with height between 65-69 inches."""