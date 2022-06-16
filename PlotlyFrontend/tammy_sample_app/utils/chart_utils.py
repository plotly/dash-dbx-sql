import plotly.express as px
import numpy as np


def generate_scatter(df, xaxis, comp):
    custom_color = {
        "sex": ["rgb(54, 127, 255)", "rgb(255, 0, 106)"],
        "Smoker": ["rgb(0, 0, 0)", "rgb(102, 255, 255)"],
        "cholesterol": ["rgb(252, 125, 5)", "rgb(65, 206, 224)"],
        "bloodpressure": ["rgb(48, 255, 69)", "rgb(252, 50, 50)"],
    }
    axis_labels = {
        "age": "Age (years)",
        "height": "Height (inches)",
        "weight": "Weight (lbs)",
    }
    scatter = px.scatter(
        df,
        x=xaxis,
        y="risk",
        color=comp,
        color_discrete_sequence=custom_color[comp],
        size="Total",
        labels={xaxis: axis_labels[xaxis]},
        title=f"Comparative Risk by Demographic",
    )
    return scatter
