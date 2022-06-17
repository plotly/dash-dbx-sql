import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
import plotly.express as px
from utils import dbx_utils, chart_utils

app = dash.Dash(__name__)
app.title = "dash-dbx"
server = app.server  # expose server variable for Procfile

users = dbx_utils.get_listofusers()
userlist = [{"label": i, "value": i} for i in users["userid"]]


app.layout = html.Div(
    [
        html.Header(
            [
                html.Img(src=app.get_asset_url("plotly_logo.png"), width="17%"),
                html.H1("Dash with Databricks"),
            ],
            style={"text-align": "center"},
        ),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Population level visualizations",
                    children=[
                        dmc.Grid(
                            [
                                html.Div(
                                    [
                                        html.Label(
                                            "Select the color comparison category: "
                                        ),
                                        dcc.Dropdown(
                                            id="comparison",
                                            options=[
                                                {"label": "Sex", "value": "sex"},
                                                {"label": "Smoker?", "value": "Smoker"},
                                                {
                                                    "label": "Cholesterol Level",
                                                    "value": "cholesterol",
                                                },
                                                {
                                                    "label": "Blood Pressure",
                                                    "value": "bloodpressure",
                                                },
                                            ],
                                            value="sex",
                                        ),
                                    ],
                                    style={
                                        "width": "60%",
                                        "text-align": "center",
                                    },
                                ),
                                dmc.Col(
                                    html.Div(
                                        [
                                            html.Label("Select the x axis category: "),
                                            dcc.RadioItems(
                                                id="scatter-x",
                                                options=[
                                                    {"label": "Age", "value": "age"},
                                                    {
                                                        "label": "Height",
                                                        "value": "height",
                                                    },
                                                    {
                                                        "label": "Weight",
                                                        "value": "weight",
                                                    },
                                                ],
                                                value="age",
                                            ),
                                            dcc.Graph(id="demographics"),
                                            dcc.Markdown(
                                                """
            The data used for this graph comes from the silver_users table
            which contains patient demographic data. A "group by" and "count" 
            aggregation combo are implemented via SQL statement. The columns 
            pulled into the Dash app are user-determined such that only data 
            that is displayed is retrieved from SQL to improve latency. The 
            "risk" column, the selected x-axis category column and the selected 
            comparison category column are pulled and a calculated column counting 
            the number of patients that fall into each unique combo of column 
            values is also pulled. The calculation happens in Databricks and data 
            is re-queried when the user changes either the x axis category or 
            comparison category.
                                                """
                                            ),
                                        ],
                                    ),
                                    span=6,
                                    style={
                                        "border": f"2px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
                                    },
                                ),
                                dmc.Col(
                                    html.Div(
                                        [
                                            html.Label("Select the y axis category: "),
                                            dcc.RadioItems(
                                                id="line-y",
                                                options=[
                                                    {
                                                        "label": "Calories Burned",
                                                        "value": "calories_burnt",
                                                    },
                                                    {
                                                        "label": "Miles Walked",
                                                        "value": "miles_walked",
                                                    },
                                                    {
                                                        "label": "Number of Steps",
                                                        "value": "num_steps",
                                                    },
                                                ],
                                                value="calories_burnt",
                                            ),
                                            dcc.Graph(id="fitness-line"),
                                            dcc.Markdown(
                                                """
            The data used for this graph comes from the silver_users and 
            silver_sensors tables. A join of the tables is done in SQL
            wherein the sensor data is matched to the demographic data for 
            that patient on the shared "user_id" column from each table.
            The fitness metrics (number of steps, burned calories, miles walked) 
            are reported by the sensors/devices for some date/time. A single SQL 
            query is used to pull the data for a user-specified fitness metric, 
            averaged by specified demographic group broken down by comparison 
            category, per day.
                                                """
                                            ),
                                        ],
                                    ),
                                    span=6,
                                    style={
                                        "border": f"2px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
                                    },
                                ),
                            ],
                            justify="center",
                            gutter="xl",
                            style={"margin-bottom": 30, "margin-top": 30},
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Select the x axis category:"
                                                ),
                                                dcc.Dropdown(
                                                    id="heat-x",
                                                    options=[
                                                        {
                                                            "label": "Age",
                                                            "value": "age",
                                                        },
                                                        {
                                                            "label": "Height",
                                                            "value": "height",
                                                        },
                                                        {
                                                            "label": "Weight",
                                                            "value": "weight",
                                                        },
                                                    ],
                                                    value="age",
                                                ),
                                            ],
                                        )
                                    ],
                                    span=3,
                                ),
                                dmc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Select the y axis category:"
                                                ),
                                                dcc.Dropdown(
                                                    id="heat-y",
                                                    options=[
                                                        {
                                                            "label": "Age",
                                                            "value": "age",
                                                        },
                                                        {
                                                            "label": "Height",
                                                            "value": "height",
                                                        },
                                                        {
                                                            "label": "Weight",
                                                            "value": "weight",
                                                        },
                                                    ],
                                                    value="height",
                                                ),
                                            ]
                                        )
                                    ],
                                    span=3,
                                ),
                                dmc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Select the fitness metric:"
                                                ),
                                                dcc.RadioItems(
                                                    id="heat-fitness",
                                                    options=[
                                                        {
                                                            "label": "Calories Burned",
                                                            "value": "calories_burnt",
                                                        },
                                                        {
                                                            "label": "Miles Walked",
                                                            "value": "miles_walked",
                                                        },
                                                        {
                                                            "label": "Number of Steps",
                                                            "value": "num_steps",
                                                        },
                                                    ],
                                                    value="calories_burnt",
                                                ),
                                            ]
                                        )
                                    ],
                                    span=3,
                                ),
                                dmc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Select the fitness metric percentile range: "
                                                ),
                                                dcc.RangeSlider(
                                                    id="slider-val",
                                                    min=1,
                                                    max=100,
                                                    step=None,
                                                    value=[1, 100],
                                                ),
                                            ]
                                        )
                                    ],
                                    span=3,
                                ),
                            ],
                            align="center",
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(id="heat-fig"),
                                                dcc.Markdown(
                                                    """
                    The data used for this graph comes from the silver_users and 
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
                    with height between 60-64 inches whereas for male patients it's in the 
                    50-54 year old range with height between 75-79 inches.
                                                    """
                                                ),
                                            ]
                                        ),
                                    ],
                                    span=12,
                                ),
                            ]
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Specific User Metrics",
                    children=[
                        dmc.Grid(
                            [
                                html.Div(
                                    [
                                        html.Label("Select a specific user: "),
                                        dcc.Dropdown(
                                            id="user-id",
                                            options=userlist,
                                            value="1",
                                        ),
                                    ],
                                    style={"width": "60%", "text-align": "center"},
                                ),
                            ],
                            justify="center",
                            gutter="xl",
                            style={"margin-bottom": 30, "margin-top": 30},
                        ),
                    ],
                ),
            ]
        ),
    ],
)


@app.callback(
    Output("demographics", "figure"),
    Input("scatter-x", "value"),
    Input("comparison", "value"),
)
def make_scatter(xaxis, comp):
    dfscatter = dbx_utils.get_scatter_data(xaxis, comp)
    scatterfig = chart_utils.generate_scatter(dfscatter, xaxis, comp)
    return scatterfig


@app.callback(
    Output("fitness-line", "figure"),
    Input("line-y", "value"),
    Input("comparison", "value"),
)
def make_line(yaxis, comp):
    dfline = dbx_utils.get_line_data(yaxis, comp)
    linefig = chart_utils.generate_line(dfline, yaxis, comp)
    return linefig


@app.callback(
    Output("heat-fig", "figure"),
    Input("heat-x", "value"),
    Input("heat-y", "value"),
    Input("heat-fitness", "value"),
    Input("comparison", "value"),
    Input("slider-val", "value"),
)
def make_heat(xaxis, yaxis, fitness, comp, slider):
    dfheat = dbx_utils.get_heat_data(xaxis, yaxis, fitness, comp, slider)
    heatfig = chart_utils.generate_heat(dfheat, xaxis, yaxis, fitness, comp)
    return heatfig


if __name__ == "__main__":
    app.run_server(debug=True)
