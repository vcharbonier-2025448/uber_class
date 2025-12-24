import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Energy Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ireland_energy.csv")

df = load_data()

st.title("Energy Domestic Supply")

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

def get_value(col):summary = (
    if col not in row.columns or row.empty:    filtered.groupby("year")[metric_col]
        return np.nan    .mean()
    return row[col].mean()    .reset_index(name=metric_col)
)
def fmt(label, val):
    if pd.isna(val):chart = alt.Chart(summary).mark_line(point=True).encode(
        return "N/A"    x="year:O",
    if "%" in label:    y=alt.Y(f"{metric_col}:Q", title=metric_col),
        return f"{val:.1f}%"    tooltip=["year", metric_col]
    return f"{val:,.3f}")

a, b = st.columns(2)st.altair_chart(chart, use_container_width=True)
c, d = st.columns(2)st.dataframe(summary, use_container_width=True)

slots = [a, b, c, d]
for (label, col), slot in zip(METRICS.items(), slots):
    val = get_value(col)
    slot.metric(label, fmt(label, val), delta=None, border=True)