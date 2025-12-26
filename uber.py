import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="Energy Dashboard", layout="wide")

def load_data():
    return pd.read_csv("energy.csv")

df = load_data()

df_ie =  pd.read_csv("ireland_energy.csv")
df_uy =  pd.read_csv("uruguay_energy.csv")

st.subheader("Quick comparison (latest year)")

col1, col2 = st.columns(2)

with col1:
    st.metric("Ireland Import Dependency", round(df_ie["import_dependency"].iloc[-1],2))
    st.metric("Ireland Renewable Share", round(df_ie["renew_prod_%"].iloc[-1]*100,1))

with col2:
    st.metric("Uruguay Import Dependency", round(df_uy["import_dependency"].iloc[-1],2))
    st.metric("Uruguay Renewable Share", round(df_uy["renew_prod_%"].iloc[-1]*100,1))
    

st.title("Energy Domestic Supply")
st.info("Uruguay shows consistently lower import dependency and higher renewable production, indicating a more advanced stage of energy transition compared to Ireland.")

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("Country", sorted(df.country.unique()))

with col2:
    year = st.slider("Year", int(df.year.min()), int(df.year.max()), 2023)

filtered = df[(df.country == country) & (df.year <= year)]

METRICS = {
    "Domestic Supply": "domestic_supply",
    "Import Dependency": "import_dependency",
    "% Renewable Production": "renew_prod_%"
}
metric_label = st.selectbox("Select metric", list(METRICS.keys()))
metric_col = METRICS[metric_label]

row = df[(df["country"] == country) & (df["year"] == year)]

def get_value(col):
    if col not in row.columns or row.empty:
        return np.nan
    return row[col].mean()

def fmt(label, val):
    if pd.isna(val):
        return "N/A"
    if "%" in label:
        return f"{val:.1f}%"
    return f"{val:,.3f}"

a, b = st.columns(2)
c, d = st.columns(2)

slots = [a, b, c, d]
for (label, col), slot in zip(METRICS.items(), slots):
    val = get_value(col)
    slot.metric(label, fmt(label, val), delta=None, border=True)

summary = (
    filtered.groupby("year")[metric_col]
    .mean()
    .reset_index(name=metric_col)
)

chart = alt.Chart(summary).mark_line(point=True).encode(
    x="year:O",
    y=alt.Y(f"{metric_col}:Q", title=metric_col),
    tooltip=["year", metric_col]
)

st.altair_chart(chart, use_container_width=True)

st.subheader("Energy Dependency vs Renewable Production")

scatter_df = pd.concat([
    df_ie.assign(country="Ireland"),
    df_uy.assign(country="Uruguay")
])

fig = plt.scatter(scatter_df,
    x="import_dependency",
    y="renew_prod_%",
    color="country",
    labels={"renew_prod_%":"Renewable Share"}
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(summary, use_container_width=True)





