import dash
from dash import dcc, html, Input, Output
import dash_mantine_components as dmc
import plotly.express as px
from utils import dbx_utils, chart_utils

app = dash.Dash(__name__)
app.title = "dash-dbx"
server = app.server  # expose server variable for Procfile

app.layout = html.Div(
    [
        html.Header(
            [
                html.Img(src=app.get_asset_url("plotly_logo.png"), width="23%"),
                html.H1("Dash with Databricks"),
            ]
        ),
        dmc.Grid(
            [
                html.Div(
                    [
                        html.Label("Select the color comparison category: "),
                        dcc.Dropdown(
                            id="comparison",
                            options=[
                                {"label": "Sex", "value": "sex"},
                                {"label": "Smoker?", "value": "Smoker"},
                                {"label": "Cholesterol Level", "value": "cholesterol"},
                                {"label": "Blood Pressure", "value": "bloodpressure"},
                            ],
                            value="sex",
                        ),
                    ],
                    style={"width": "60%", "text-align": "center"},
                ),
                dmc.Col(
                    html.Div(
                        [
                            html.Label("Select the x axis category: "),
                            dcc.RadioItems(
                                id="scatter-x",
                                options=[
                                    {"label": "Age", "value": "age"},
                                    {"label": "Height", "value": "height"},
                                    {"label": "Weight", "value": "weight"},
                                ],
                                value="age",
                            ),
                            dcc.Graph(id="demographics"),
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
                                    {"label": "Miles Walked", "value": "miles_walked"},
                                    {"label": "Number of Steps", "value": "num_steps"},
                                ],
                                value="calories_burnt",
                            ),
                            dcc.Graph(id="fitness-line"),
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
        ),
    ],
)


@app.callback(
    Output("demographics", "figure"),
    Output("fitness-line", "figure"),
    Input("scatter-x", "value"),
    Input("line-y", "value"),
    Input("comparison", "value"),
)
def make_graphs(xaxis, yaxis, comp):
    dfscatter = dbx_utils.get_user_data(xaxis, comp)
    dfline = dbx_utils.join_user_sensor(yaxis, comp)
    scatterfig = chart_utils.generate_scatter(dfscatter, xaxis, comp)
    linefig = chart_utils.generate_line(dfline, yaxis, comp)
    return scatterfig, linefig


if __name__ == "__main__":
    app.run_server(debug=True)
