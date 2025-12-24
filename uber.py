import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Energy Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

st.title("Energy Domestic Supply")

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("Country", sorted(df.country.unique()))

with col2:
    year = st.slider("Year", int(df.year.min()), int(df.year.max()), 2023)

filtered = df[(df.country == country) & (df.year <= year)]

summary = (
    filtered.groupby("year")["yaxis_ratio"]
    .mean()
    .reset_index(name="Domestic Supply")
)

chart = alt.Chart(summary).mark_line(point=True).encode(
    x="year:O",
    y="Domestic Supply:Q",
    tooltip=["year","Domestic Supply"]
)

st.altair_chart(chart, use_container_width=True)
st.dataframe(summary, use_container_width=True)