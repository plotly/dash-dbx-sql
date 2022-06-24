import plotly.express as px
from constants import custom_color


def fig_style(fig):
    return (
        fig.update_layout(
            paper_bgcolor="#1c2022", plot_bgcolor="#1c2022", font_color="#A3AAB7"
        )
        .update_xaxes(gridcolor="#3F3F3F")
        .update_yaxes(gridcolor="#3F3F3F")
    )


def create_empty(text):
    layout = dict(
        autosize=True,
        annotations=[dict(text=text, showarrow=False)],
        paper_bgcolor="#1c2022",
        plot_bgcolor="#1c2022",
        font_color="#A3AAB7",
        font=dict(color="FFFF", size=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )
    return {"data": [], "layout": layout}


def generate_scatter(df, xaxis, comp):
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
    return fig_style(fig)


def generate_line(df, yaxis, comp):
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
    return fig_style(fig)


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

    colorscale = [
        "#1d2022",
        "#330e09",
        "#651c12",
        "#a72e1e",
        "#db4c39",
        "#e7887b",
    ]  # "#1d2022","#44201a","#5d221b","#74261d","#892b21","#9e3226","#b3392b","#c74232","#db4c39"
    fig = px.density_heatmap(
        df,
        x=axis1,
        y=axis2,
        z=f"{fitness}tot",
        histfunc="avg",
        facet_col=comp,
        color_continuous_scale=colorscale,
        nbinsx=bin_sizes[axis1],
        nbinsy=bin_sizes[axis2],
        labels={
            axis1: axis_labels[axis1],
            axis2: axis_labels[axis2],
            fitness: axis_labels[fitness],
            comp: axis_labels[comp],
        },
    )
    return fig_style(fig)


def generate_userbar(df, yaxis, user):
    axis_labels = {
        "calories_burnt": "Daily Burned Calories",
        "miles_walked": "Miles Walked Daily",
        "num_steps": "Total Daily Steps",
    }
    fig = px.bar(
        df,
        x="date",
        y=f"{yaxis}",
        labels={f"{yaxis}": axis_labels[yaxis]},
        title=f"{axis_labels[yaxis]} for patient {user}",
        text_auto=True,
    )
    fig.update_traces(marker_color="#972a1b")
    return fig_style(fig)
