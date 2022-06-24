from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils import dbx_utils
from constants import demographics_data_dict, heatmap_data_dict, fitness_data_dict


def create_text_columns(data_dict, class_name=None):
    """Create element that creates header + text column for every header and text in the list"""
    width = {"width": str(100 / len(data_dict["headers"])) + "%"}
    return html.Div(
        [
            html.Div([html.H3(header), html.P(text)], style=width)
            for header, text in zip(data_dict["headers"], data_dict["texts"])
        ],
        className="text-columns" + (f" {class_name}" if class_name else ""),
    )


def generate_usercomp(df, user, fitness):
    useridx = df.index[df["user_id"] == int(user)].to_list()[0]
    num_pat = len(df)
    if useridx == 0:
        usercomp = dmc.Text(
            f"Of the {num_pat} patients in the study, Patient {user} had the lowest total {fitness.lower()}"
        )
    elif useridx == num_pat - 1:
        usercomp = dmc.Text(
            f"Of the {num_pat} patients in the study, Patient {user} had the highest total {fitness.lower()}"
        )
    else:
        percentile = round((useridx + 1) / num_pat * 100, 2)
        usercomp = dmc.Text(
            f"Patient  had higher total {fitness.lower()} than {percentile}% of the {num_pat} patients in the study"
        )
    return usercomp


def notification_user(text):
    return dmc.Notification(
        id="notify-user",
        title="User Data",
        message=[text],
        disallowClose=True,
        radius="xl",
        icon=[DashIconify(icon="simple-icons:databricks", color="#DB4C39", width=128)],
        action="show",
    )


def notification_scatter(text):
    return dmc.Notification(
        id="notify-scatter",
        title="Risk Data",
        message=[text],
        disallowClose=True,
        radius="xl",
        icon=[DashIconify(icon="simple-icons:databricks", color="#DB4C39", width=128)],
        action="show",
    )


def notification_line(text):
    return dmc.Notification(
        id="notify-line",
        title="Daily Fitness Data",
        message=[text],
        disallowClose=True,
        radius="xl",
        icon=[DashIconify(icon="simple-icons:databricks", color="#DB4C39", width=128)],
        action="show",
    )


def notification_heatmap(text, action):
    return dmc.Notification(
        id="notify-heatmap",
        title="Heatmap Data",
        message=[text],
        disallowClose=True,
        radius="xl",
        icon=[DashIconify(icon="simple-icons:databricks", color="#DB4C39", width=128)],
        action=action,
    )


def header(
    app, header_color, header, subheader=None, header_background_color="transparent"
):

    logo = html.Img(src=app.get_asset_url("images/plotly-logo-dark-theme.png"))
    dash_logo = html.A(
        logo,
        href="https://plotly.com/dash/",
        target="_blank",
        className="header-logos-left",
    )

    header = html.Div(
        [
            html.Div(
                [
                    html.Div("Dash", style={"color": "#7976F7"}),
                    html.Div(" with ", style={"padding": "0px 15px"}),
                    html.Div(" Databricks", style={"color": "#DB4C39"}),
                ],
                className="header-title",
            ),
            html.Div(subheader, className="subheader-title"),
        ],
        style={"color": header_color},
        className="header-text-middle",
    )

    logo = html.Img(src=app.get_asset_url("images/databricks.png"))
    databricks_logo = html.A(
        logo,
        href="https://databricks.com/",
        target="_blank",
        className="header-logos-right",
    )

    return html.Div(
        [dash_logo, header, databricks_logo],
        className="header",
        style={"background-color": header_background_color},
    )


LEFT_TAB = html.Div(
    [
        # CROSS FILTER
        dmc.Group(
            direction="column",
            position="center",
            class_name="global-control",
            children=[
                dmc.Title("Query data by:"),
                dmc.Chips(
                    id="comparison",
                    value="sex",
                    direction="row",
                    align="center",
                    variant="filled",
                    color="orange",
                    data=[
                        {
                            "label": "Blood Pressure",
                            "value": "bloodpressure",
                        },
                        {"label": "Sex", "value": "sex"},
                        {"label": "Smoker?", "value": "Smoker"},
                        {
                            "label": "Cholesterol Level",
                            "value": "cholesterol",
                        },
                    ],
                ),
            ],
        ),
        # TOP 2 FIGURES
        dmc.Grid(
            gutter="xl",
            children=[
                dmc.Col(
                    span=6,
                    children=html.Div(
                        className="card",
                        children=[
                            # html.Label("Select the x axis category: "),
                            dmc.SegmentedControl(
                                id="scatter-x",
                                fullWidth=True,
                                value="height",
                                data=[
                                    {"label": "Age", "value": "age"},
                                    {"label": "Height", "value": "height"},
                                    {"label": "Weight", "value": "weight"},
                                ],
                            ),
                            dmc.LoadingOverlay(
                                dcc.Graph(
                                    id="demographics",
                                    className="glow",
                                    config={"displayModeBar": False},
                                ),
                                overlayOpacity=0.95,
                                overlayColor="#1D2022",
                                loaderProps=dict(color="orange", variant="bars"),
                            ),
                            html.Div(
                                [
                                    html.Img(src="assets/images/sql_demographics.png"),
                                    create_text_columns(
                                        demographics_data_dict, "tooltiptext"
                                    ),
                                ],
                                className="tooltip",
                            ),
                        ],
                    ),
                ),
                dmc.Col(
                    span=6,
                    children=html.Div(
                        className="card",
                        children=[
                            dmc.SegmentedControl(
                                id="line-y",
                                # label="Select the y axis category:",
                                fullWidth=True,
                                data=[
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
                            dmc.LoadingOverlay(
                                dcc.Graph(
                                    id="fitness-line",
                                    className="glow",
                                    config={"displayModeBar": False},
                                ),
                                overlayOpacity=0.95,
                                overlayColor="#1D2022",
                                loaderProps=dict(color="orange", variant="bars"),
                            ),
                            html.Div(
                                [
                                    html.Img(src="assets/images/sql_fitness.png"),
                                    create_text_columns(
                                        fitness_data_dict, "tooltiptext"
                                    ),
                                ],
                                className="tooltip",
                            ),
                        ],
                    ),
                ),
            ],
        ),
        html.Div(
            className="card card-centre",
            children=[
                ## HEAT MAP - CONTROLS
                dmc.Grid(
                    align="flex-end",
                    justify="center",
                    # grow=True,
                    children=[
                        dmc.Col(
                            span=4,
                            children=[
                                html.Label("Filter by performance percentile"),
                                dcc.RangeSlider(
                                    id="slider-val",
                                    min=1,
                                    max=100,
                                    value=[1, 100],
                                    allowCross=False,
                                ),
                            ],
                        ),
                        dmc.Col(
                            span=4,
                            children=dmc.Center(
                                dmc.SegmentedControl(
                                    id="heat-fitness",
                                    value="calories_burnt",
                                    data=[
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
                                )
                            ),
                        ),
                        dmc.Col(
                            span=4,
                            children=[
                                dmc.MultiSelect(
                                    id="heat-axes",
                                    label="Choose displayed data",
                                    data=["age", "height", "weight"],
                                    value=["age", "height"],
                                    maxSelectedValues=2,
                                )
                            ],
                            style={"padding-bottom": "2vh"},
                        ),
                    ],
                ),
                ## HEAT MAP - FIGURE
                dmc.LoadingOverlay(
                    dcc.Graph(
                        id="heat-fig",
                        className="glow",
                        config={"displayModeBar": False},
                    ),
                    overlayOpacity=0.95,
                    overlayColor="#1D2022",
                    loaderProps=dict(color="orange", variant="bars"),
                ),
                html.Div(
                    [
                        html.Img(src="assets/images/sql_heatmap.png"),
                        create_text_columns(heatmap_data_dict, "tooltiptext"),
                    ],
                    className="tooltip",
                ),
            ],
        ),
    ],
    className="left-tab",
)


RIGHT_TAB = html.Div(
    [
        dmc.Grid(
            justify="center",
            gutter="xl",
            children=[
                dmc.Col(
                    dmc.Title(
                        "Patient 19's fitness data",
                        id="user-header",
                        align="center",
                        order=1,
                    ),
                    span=10,
                ),
                dmc.Col(
                    span=10,
                    children=[
                        dmc.Grid(
                            class_name="card",
                            children=[
                                ## User selection
                                dmc.SegmentedControl(
                                    id="user-id",
                                    value="19",
                                    fullWidth=True,
                                    data=dbx_utils.get_listofusers(dash_prepare=True),
                                ),
                                ## USER TEXT INFO 1
                                dmc.Col(
                                    dmc.LoadingOverlay(
                                        id="user-demo",
                                        overlayOpacity=0.95,
                                        overlayColor="#1D2022",
                                        loaderProps=dict(
                                            color="orange", variant="dots"
                                        ),
                                        class_name="user-demo-border",
                                    ),
                                    span=6,
                                ),
                                ## USER TEXT INFO 2
                                dmc.Col(
                                    dmc.LoadingOverlay(
                                        id="user-comp",
                                        overlayOpacity=0.95,
                                        overlayColor="#1D2022",
                                        loaderProps=dict(
                                            color="orange", variant="dots"
                                        ),
                                    ),
                                    span=6,
                                ),
                            ],
                        ),
                    ],
                ),
                ## FIGURE
                dmc.Col(
                    span=10,
                    children=[
                        ## METRIC FILTER
                        dmc.SegmentedControl(
                            id="user-fit",
                            # label="Select the fitness metric:",
                            value="calories_burnt",
                            fullWidth=True,
                            data=[
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
                        ),
                        ## FIGURE
                        dmc.LoadingOverlay(
                            dcc.Graph(
                                id="user-metrics-fig",
                                className="glow",
                                config={"displayModeBar": False},
                            ),
                            overlayOpacity=0.95,
                            overlayColor="#1D2022",
                            loaderProps=dict(color="orange", variant="bars"),
                        ),
                    ],
                ),
            ],
        ),
    ],
    className="right-tab",
)
