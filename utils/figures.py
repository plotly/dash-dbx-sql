import plotly.express as px
import numpy as np
import dash_mantine_components as dmc


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
    fig = px.scatter(
        df,
        x=xaxis,
        y="risk",
        color=comp,
        color_discrete_sequence=custom_color[comp],
        size="Total",
        labels={xaxis: axis_labels[xaxis]},
        title=f"Comparative Risk by Demographic",
    )
    fig.update_layout(paper_bgcolor='#1c2022', plot_bgcolor="#1c2022", font_color="#A3AAB7")
    return fig


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
    fig = px.line(
        df,
        x="date",
        y=f"{yaxis}tot",
        color=comp,
        color_discrete_sequence=custom_color[comp],
        markers=True,
        labels={f"{yaxis}tot": axis_labels[yaxis]},
        title=f"Comparative Daily Fitness Metrics by Demographic",
    )
    fig.update_layout(paper_bgcolor='#1c2022', plot_bgcolor="#1c2022", font_color="#A3AAB7")
    return fig


def generate_heat(df, axis1, axis2, fitness, comp):
    axis_labels = {
        "calories_burnt": "Calories Burned Daily",
        "miles_walked": "Miles Walked Daily",
        "num_steps": "Total Daily Steps",
        "sex": "Sex",
        "Smoker": "Smoker?",
        "cholesterol": "Cholesterol Level",
        "bloodpressure": "Blood Pressure",
        "age": "Age (years)",
        "height": "Height (inches)",
        "weight": "Weight (lbs)",
    }
    bin_sizes = {"age": 10, "height": 5, "weight": 20}
    fig = px.density_heatmap(
        df,
        x=axis1,
        y=axis2,
        z=f"{fitness}tot",
        histfunc="avg",
        facet_col=comp,
        nbinsx=bin_sizes[axis1],
        nbinsy=bin_sizes[axis2],
        labels={
            axis1: axis_labels[axis1],
            axis2: axis_labels[axis2],
            fitness: axis_labels[fitness],
            comp: axis_labels[comp],
        },
    )
    fig.update_layout(paper_bgcolor='#1c2022', plot_bgcolor="#1c2022", font_color="#A3AAB7")
    return fig


def generate_userbar(df, yaxis, user):
    axis_labels = {
        "calories_burnt": "Calories Burned Daily",
        "miles_walked": "Miles Walked Daily",
        "num_steps": "Total Daily Steps",
    }
    fig = px.bar(
        df,
        x="date",
        y=f"{yaxis}",
        labels={f"{yaxis}": axis_labels[yaxis]},
        title=f"{axis_labels[yaxis]} for user with ID: {user}",
        text_auto=True,
    )
    fig.update_layout(paper_bgcolor='#1c2022', plot_bgcolor="#1c2022", font_color="#A3AAB7",)
    return fig