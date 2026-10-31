import plotly.express as px


def bar_chart(
    df,
    x,
    y="Vehicles",
    title=""
):

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=y,
        text=y,
        title=title
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=450
    )

    return fig