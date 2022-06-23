from pydoc import classname
from dash import html, dcc
import dash_mantine_components as dmc

from utils import dbx_utils
from constants import TEXT_DEMOGRAPHICS, TEXT_FITNESS_LINE, TEXT_HEAT_FIG

def header(app, header_color, header, subheader=None, header_background_color="transparent"):
    
    logo = html.Img(src=app.get_asset_url("images/databricks.png"))
    databricks_logo = html.A(logo, href="https://databricks.com/", target="_blank", className="header-logos-left")

    header = html.Div([
            html.Div(header, className="header-title"),
            html.Div(subheader, className="subheader-title"),
        ],
        style={"color": header_color},
        className="header-text-middle"
    )

    logo = html.Img(src=app.get_asset_url("images/plotly-logo-dark-theme.png"))
    dash_logo = html.A(logo, href="https://plotly.com/dash/", target="_blank", className="header-logos-right")


    
    return html.Div([databricks_logo, header, dash_logo], className="header", style={"background-color": header_background_color})


LEFT_TAB = html.Div([

    # GLOBAL CONTROL
    dmc.Paper([
        dmc.Select(
            id="comparison",
            # label="Select the color comparison category:",
            value="sex",
            data=[
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
        )
    ], class_name="global-control"),

    # TOP 2 FIGURES
    dmc.Grid(
        justify="center",
        gutter="xl",
        # style={"margin-bottom": 30, "margin-top": 30},
        children=[

            dmc.Col(
                span=6,
                class_name="card",
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
                        dcc.Graph(id="demographics", className="glow"),
                        loaderProps=dict(variant="bars")
                    ),
                    dmc.Text(TEXT_DEMOGRAPHICS, size="md")
                ]
            ),

            dmc.Col(
                span=6,
                class_name="card",
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
                        dcc.Graph(id="fitness-line"),
                        loaderProps=dict(variant="bars")
                    ),
                    dmc.Text(TEXT_FITNESS_LINE, size="md"),
                ]
            )
        ],
    ),
    
    html.Div(
        className="card",
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
                        html.Label("Select the fitness metric percentile range:"),
                        dcc.RangeSlider(
                            id="slider-val",
                            min=1,
                            max=100,
                            step=None,
                            value=[1, 100],
                        ),
                    ]),

                    dmc.Col(
                        span=4,
                        children=
                        dmc.Center(dmc.SegmentedControl(
                            id="heat-fitness",
                            # label="Select the fitness metric:",
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
                        )),
                    ),
                        
                    dmc.Col(
                        span=4,
                        children=[
                            dmc.MultiSelect(
                                id="heat-axes",
                                label="Select the heat plot axes:",
                                # description="You must select 2 axes categories",
                                data=["age", "height", "weight"],
                                value=["age", "height"],
                                maxSelectedValues=2,
                            )
                        ]
                    ),
                ]
            ),
            ## HEAT MAP - FIGURE
            dmc.LoadingOverlay(
                dcc.Graph(id="heat-fig"),
                loaderProps=dict(variant="bars")
            ),
            dmc.Text(TEXT_HEAT_FIG, size="md"),
        ]
    )

], className="left-tab")


RIGHT_TAB = html.Div([
    dmc.Grid(
        justify="center",
        gutter="xl",
        # style={"margin-bottom": 30, "margin-top": 30},
        children=[
        
        ## USER SELECTION
        dmc.Col(
            span=10,
            children=[
            dmc.Select(
                id="user-id",
                label="Select a specific user:",
                data=dbx_utils.get_listofusers(dash_prepare=True),
                value="1",
            ),
        ]),

            
        dmc.Col(
            span=10,
            children=dmc.Grid(class_name="card",children=[
                ## USER TEXT INFO 1
                dmc.Col(
                    id="user-demo",
                    class_name="user-demo-border",
                    span=5,
                    # style={"border": f"2px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}"},
                ),


                ## USER TEXT INFO 2
                dmc.Col(
                    id="user-comp",
                    span=5,
                    # style={"border": f"2px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",},
                ),
            ]),
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
                    dcc.Graph(id="user-metrics-fig"),
                    loaderProps=dict(variant="bars")
                ),
            ]
        ),
    ]),
], className="right-tab")