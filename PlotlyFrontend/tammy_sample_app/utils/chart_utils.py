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


def generate_line(df, yaxis, comp):
    custom_color = {
        "sex": ["rgb(54, 127, 255)", "rgb(255, 0, 106)"],
        "Smoker": ["rgb(0, 0, 0)", "rgb(102, 255, 255)"],
        "cholesterol": ["rgb(252, 125, 5)", "rgb(65, 206, 224)"],
        "bloodpressure": ["rgb(48, 255, 69)", "rgb(252, 50, 50)"],
    }
    axis_labels = {
        "calories_burnt": "Calories Burned Daily",
        "miles_walked": "Miles Walked Daily",
        "num_steps": "Total Daily Steps",
    }
    line = px.line(
        df,
        x="date",
        y=f"{yaxis}tot",
        color=comp,
        color_discrete_sequence=custom_color[comp],
        markers=True,
        labels={f"{yaxis}tot": axis_labels[yaxis]},
        title=f"Comparative Daily Fitness Metrics by Demographic",
    )
    return line
