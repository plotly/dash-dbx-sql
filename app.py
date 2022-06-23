from dash import Dash, html, Input, Output, callback
import dash_mantine_components as dmc
import plotly.express as px
from skimage import io

from utils import dbx_utils, figures
import utils.components as comp

app = Dash(__name__, title="dash-dbx")
server = app.server  # expose server variable for Procfile


## add notifications
## databricks loading logo
## top text - 3/4 horizontal bullet points # .bullet-points 

app.layout = dmc.MantineProvider(
    withGlobalStyles=True,
    theme={"colorScheme": "dark",
    "backgroundColor": "red"},
    children=[
        ## Header,
        comp.header(app, "#FFFFFF", "Dash with Databricks", header_background_color="#111014"),
        html.P(""""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""),
        ## Tab Selection and their Content 
        dmc.Tabs(
            grow=True,
            variant="outline",
            children=[
                dmc.Tab(label="Population level visualizations", children=comp.LEFT_TAB),
                dmc.Tab(label="Specific User Metrics", children=comp.RIGHT_TAB),
            ]
        )
    ]
)


@callback(
    Output("user-demo", "children"),
    Output("user-metrics-fig", "figure"),
    Output("user-comp", "children"),
    Input("user-id", "value"),
    Input("user-fit", "value"),
)
def make_userpage(userid, fitness):
    dfuserdemo, dfuserfit = dbx_utils.get_user_data(int(userid), fitness)
    user_demo = [
        dmc.Text(
            f"Patient {userid} is a {dfuserdemo['age'][0]} year old, {dfuserdemo['weight'][0]} lbs {dfuserdemo['sex'][0].lower()}, {dfuserdemo['Smoker'][0].lower()}"
        ),
        dmc.Text(f"Patient {userid} Cholesterol Level: {dfuserdemo['cholesterol'][0]}"),
        dmc.Text(
            f"Patient {userid} Blood Pressure Level: {dfuserdemo['bloodpressure'][0]}"
        ),
    ]
    userfig = figures.generate_userbar(dfuserfit, fitness, userid)
    dfusercomp = dbx_utils.get_user_comp(fitness)
    usercomp = figures.generate_usercomp(dfusercomp, userid, fitness)
    return user_demo, userfig, usercomp


@callback(
    Output("demographics", "figure"),
    Input("scatter-x", "value"),
    Input("comparison", "value"),
)
def make_scatter(xaxis, comp):
    dfscatter = dbx_utils.get_scatter_data(xaxis, comp)
    scatterfig = figures.generate_scatter(dfscatter, xaxis, comp)
    return scatterfig


@callback(
    Output("fitness-line", "figure"),
    Input("line-y", "value"),
    Input("comparison", "value"),
)
def make_line(yaxis, comp):
    dfline = dbx_utils.get_line_data(yaxis, comp)
    linefig = figures.generate_line(dfline, yaxis, comp)
    return linefig


@callback(
    Output("heat-fig", "figure"),
    Input("heat-axes", "value"),
    Input("heat-fitness", "value"),
    Input("comparison", "value"),
    Input("slider-val", "value"),
)
def make_heat(axes, fitness, comp, slider):
    if len(axes) == 2:
        dfheat = dbx_utils.get_heat_data(axes[0], axes[1], fitness, comp, slider)
        heatfig = figures.generate_heat(dfheat, axes[0], axes[1], fitness, comp)
    else:
        img = io.imread("assets/images/no_show.png")
        heatfig = px.imshow(img)
    return heatfig


if __name__ == "__main__":
    app.run_server(debug=True)
