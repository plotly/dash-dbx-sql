from dash import Dash, html, Input, Output, callback
import dash_mantine_components as dmc
import plotly.express as px
from skimage import io

from utils import dbx_utils, figures
import utils.components as comp

app = Dash(__name__, title="dash-dbx")
server = app.server  # expose server variable for Procfile


## databricks loading logo
## top text - 3/4 horizontal bullet points # .bullet-points 

app.layout = dmc.MantineProvider(
    withGlobalStyles=True,
    theme={"colorScheme": "dark"},
    children=dmc.NotificationsProvider([
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
        ),
        html.Div(id="notifications-user"),
        html.Div(id="notifications-scatter"),
        html.Div(id="notifications-line"),
        html.Div(id="notifications-heatmap"),
    ])
)


@callback(
    Output("user-demo", "children"),
    Output("user-metrics-fig", "figure"),
    Output("user-comp", "children"),
    Output("notifications-user", "children"),
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
    usercomp = comp.generate_usercomp(dfusercomp, userid, fitness)

    notification = f"User data loaded. \n\n3 queries executed with number of rows retrieved: {len(dfuserdemo) + len(dfuserfit) + len(dfusercomp)}"
    return user_demo, userfig, usercomp, comp.notification_user(notification)


@callback(
    Output("demographics", "figure"),
    Output("notifications-scatter", "children"),
    Input("scatter-x", "value"),
    Input("comparison", "value"),
)
def make_scatter(xaxis, comparison):
    dfscatter = dbx_utils.get_scatter_data(xaxis, comparison)
    scatterfig = figures.generate_scatter(dfscatter, xaxis, comparison)
    notification = f"Scatter data loaded. \n1 query executed with number of rows retrieved: {len(dfscatter)}"
    return scatterfig, comp.notification_scatter(notification)


@callback(
    Output("fitness-line", "figure"),
    Output("notifications-line", "children"),
    Input("line-y", "value"),
    Input("comparison", "value"),
)
def make_line(yaxis, comparison):
    dfline = dbx_utils.get_line_data(yaxis, comparison)
    linefig = figures.generate_line(dfline, yaxis, comparison)
    notification = f"Scatter data loaded. \n1 query executed with number of rows retrieved: {len(dfline)}"
    return linefig, comp.notification_line(notification)


@callback(
    Output("heat-fig", "figure"),
    Output("notifications-heatmap", "children"),
    Input("heat-axes", "value"),
    Input("heat-fitness", "value"),
    Input("comparison", "value"),
    Input("slider-val", "value"),
)
def make_heat(axes, fitness, comparison, slider):
    if len(axes) == 2:
        dfheat = dbx_utils.get_heat_data(axes[0], axes[1], fitness, comparison, slider)
        heatfig = figures.generate_heat(dfheat, axes[0], axes[1], fitness, comparison)
        notification, action = f"Scatter data loaded. \n1 query executed with number of rows retrieved: {len(dfheat)}", "show"
    else:
        img = io.imread("assets/images/no_show.png")
        heatfig = px.imshow(img)
        notification, action = "", "hide"
    return heatfig, comp.notification_heatmap(notification, action)


if __name__ == "__main__":
    app.run_server(debug=True)
