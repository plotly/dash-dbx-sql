import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from utils import dbx_utils, chart_utils

app = dash.Dash(__name__)
app.title = "dash-dbx"
server = app.server  # expose server variable for Procfile

app.layout = html.Div(
    [
        html.Header(
            [
                html.Img(src=app.get_asset_url("plotly_logo.png"), width="20%"),
                html.H1("Dash with Databricks"),
            ]
        ),
        html.Div(
            [
                html.Label("Select the x axis category: "),
                dcc.Dropdown(
                    id="scatter-x",
                    options=[
                        {"label": "Age", "value": "age"},
                        {"label": "Height", "value": "height"},
                        {"label": "Weight", "value": "weight"},
                    ],
                    value="age",
                ),
            ],
            style={"width": "50%"},
        ),
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
            style={"width": "50%"},
        ),
        html.Div(
            [dcc.Graph(id="demographics")],
            style={"width": "50%", "height": 450},
        ),
    ],
)


@app.callback(
    Output("demographics", "figure"),
    Input("scatter-x", "value"),
    Input("comparison", "value"),
)
def make_demographics(xaxis, comp):
    df = dbx_utils.get_user_data(xaxis, comp)
    fig = chart_utils.generate_scatter(df, xaxis, comp)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
