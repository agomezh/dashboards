import altair as alt
import app.login
import pandas as pd
import pandas_profiling as pp
import streamlit as st


def sidebar_run():

    return ""


def mainpage_run():
    st.button("run")
    st.write("# Demo dashboard")
    df = pd.read_csv("./data/iris.csv")

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.write("## Upload and download files")
        file_up = st.file_uploader("Upload your own file", type="xlsx")
        st.download_button("Get data", df.to_csv().encode("utf-8"), "iris.csv")

    with col2:
        st.markdown("## Data")
        st.write(df)

    with col3:
        st.markdown("## Data uploaded")
        st.markdown("Many things can be done... but for now, the name of the file:")
        if file_up:
            st.write(file_up.name)

    col1, col2, col3 = st.columns(3)

    with col1:
        val_1 = df.columns[0]
        val_2 = df.columns[1]
        st.write("## Simple chart")
        st.bar_chart(df[[val_1, val_2]])

    with col2:
        st.write("## Interactive chart (move the mouse over a point)")
        cols = df.columns
        alt_chart = (
            alt.Chart(df)
            .mark_circle()
            .encode(
                x=cols[0],
                y=cols[1],
                color=cols[4],
                tooltip=[cols[0], cols[1]],
            )
        )
        st.altair_chart(alt_chart, use_container_width=True)

    with col3:
        st.write("Select options")
        x_axis = st.selectbox("x axis", df.columns)
        y_axis = st.selectbox("y axis", df.columns)
        alt_chart_2 = alt.Chart(df).mark_line().encode(x=x_axis, y=y_axis)
        st.altair_chart(alt_chart_2, use_container_width=True)

    st.line_chart(df[["sepal_length", "petal_length"]])

    return "---"


if __name__ == "__main__":
    a = 1 + 1
