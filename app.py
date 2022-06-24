from dash import Dash, dcc, html, Input, Output, callback
import dash_mantine_components as dmc
import datetime as dt

from utils import dbx_utils, figures
import utils.components as comp
from constants import app_description

app = Dash(__name__, title="dash-dbx", update_title=None)
server = app.server

app.layout = dmc.MantineProvider(
    withGlobalStyles=True,
    theme={"colorScheme": "dark"},
    children=dmc.NotificationsProvider(
        [
            ## Header and app description
            comp.header(
                app,
                "#FFFFFF",
                "Dash with Databricks",
                header_background_color="#111014",
            ),
            comp.create_text_columns(app_description, "description"),
            ## Tab Selection and their Content
            dmc.Tabs(
                grow=True,
                variant="outline",
                children=[
                    dmc.Tab(
                        label="Population level visualizations", children=comp.LEFT_TAB
                    ),
                    dmc.Tab(label="Specific User Metrics", children=comp.RIGHT_TAB),
                ],
            ),
            ## Notification containers and affixes
            html.Div(id="notifications-user"),
            html.Div(id="notifications-scatter"),
            html.Div(id="notifications-line"),
            html.Div(id="notifications-heatmap"),
            dcc.Interval(id="interval", interval=1_000),
            dmc.Affix(
                html.A(
                    "See code",
                    href="https://github.com/plotly/dash-dbx-sql",
                    target="_blank",
                    className="demo-button",
                ),
                position={"bottom": 40, "left": 20},
            ),
            dmc.Affix(dmc.Text(id="time"), position={"bottom": 5, "left": 5}),
        ]
    ),
)


@callback(Output("time", "children"), Input("interval", "n_intervals"))
def refresh_data_at_interval(interval_trigger):
    """
    This simple callback demonstrates how to use the Interval component to update data at a regular interval.
    This particular example updates time every second, however, you can subsitute this data query with any acquisition method your product requires.
    """
    return dt.datetime.now().strftime("%M:%S")


@callback(
    Output("user-demo", "children"),
    Output("user-comp", "children"),
    Output("user-header", "children"),
    Output("user-metrics-fig", "figure"),
    Output("notifications-user", "children"),
    Input("user-id", "value"),
    Input("user-fit", "value"),
)
def make_userpage(userid, fitness):
    df_userdemo, df_userfit = dbx_utils.get_user_data(int(userid), fitness)
    fig_user = figures.generate_userbar(df_userfit, fitness, userid)
    df_usercomp = dbx_utils.get_user_comp(fitness)

    header = f"Patient {userid}'s fitness data"
    user_comparison = comp.generate_usercomp(df_usercomp, userid, fitness)
    blood_pressure = dmc.Text(
        f"Blood Pressure Level: {df_userdemo['bloodpressure'][0]}"
    )
    chorestelor = dmc.Text(f"Cholesterol Level: {df_userdemo['cholesterol'][0]}")
    patient_info = dmc.Text(
        f"Patient is a {df_userdemo['age'][0]} old {df_userdemo['sex'][0].lower()}, weights {df_userdemo['weight'][0]} lbs, and is a {df_userdemo['Smoker'][0].lower()}"
    )

    notification = f"User data loaded. \n\n3 queries executed with number of rows retrieved: {len(df_userdemo) + len(df_userfit) + len(df_usercomp)}"
    return (
        [patient_info, chorestelor],
        [user_comparison, blood_pressure],
        header,
        fig_user,
        comp.notification_user(notification),
    )


@callback(
    Output("demographics", "figure"),
    Output("notifications-scatter", "children"),
    Input("scatter-x", "value"),
    Input("comparison", "value"),
)
def make_scatter(xaxis, comparison):
    df_scatter = dbx_utils.get_scatter_data(xaxis, comparison)
    fig_scatter = figures.generate_scatter(df_scatter, xaxis, comparison)
    notification = f"Scatter data loaded. \n1 query executed with number of rows retrieved: {len(df_scatter)}"
    return fig_scatter, comp.notification_scatter(notification)


@callback(
    Output("fitness-line", "figure"),
    Output("notifications-line", "children"),
    Input("line-y", "value"),
    Input("comparison", "value"),
)
def make_line(yaxis, comparison):
    df_line = dbx_utils.get_line_data(yaxis, comparison)
    fig_line = figures.generate_line(df_line, yaxis, comparison)
    notification = f"Scatter data loaded. \n1 query executed with number of rows retrieved: {len(df_line)}"
    return fig_line, comp.notification_line(notification)


@callback(
    Output("heat-fig", "figure"),
    Output("notifications-heatmap", "children"),
    Input("heat-axes", "value"),
    Input("heat-fitness", "value"),
    Input("comparison", "value"),
    Input("slider-val", "value"),
)
def make_heatmap(axes, fitness, comparison, slider):
    if len(axes) == 2:
        df_heat = dbx_utils.get_heat_data(axes[0], axes[1], fitness, comparison, slider)
        fig_heat = figures.generate_heat(df_heat, axes[0], axes[1], fitness, comparison)
        notification, action = (
            f"Scatter data loaded. \n1 query executed with number of rows retrieved: {len(df_heat)}",
            "show",
        )
    else:
        text = "You must select exactly 2 axes for this plot to display!"
        fig_heat = figures.create_empty(text)
        notification, action = "", "hide"
    return fig_heat, comp.notification_heatmap(notification, action)


if __name__ == "__main__":
    app.run_server(debug=True)
