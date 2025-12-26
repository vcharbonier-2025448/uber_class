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
    

st.title("Energy Domestic Supply")
st.info("Uruguay shows consistently lower import dependency and higher renewable production, indicating a more advanced stage of energy transition compared to Ireland.")

# --- Controls (left) + KPI cards (right) ---
left, right = st.columns([2, 3])

with left:
    country = st.selectbox("Country", sorted(df["country"].unique()))

    metric_label = st.selectbox("Select metric", list(METRICS.keys()))
    metric_col = METRICS[metric_label]

    year = st.slider("Year", int(df["year"].min()), int(df["year"].max()), int(df["year"].max()))

# Filter after controls
filtered = df[(df["country"] == country) & (df["year"] <= year)]
row = df[(df["country"] == country) & (df["year"] == year)]

def get_value(col):
    if row.empty or col not in row.columns:
        return np.nan
    return float(row[col].mean())

def fmt(label, val):
    if pd.isna(val):
        return "N/A"
    if "%" in label:
        return f"{val*100:.1f}%"
    return f"{val:.3f}"

# --- KPI cards (2x2) on the right ---
with right:
    r1c1, r1c2 = st.columns(2)
    r2c1, r2c2 = st.columns(2)

    r1c1.metric("Import Dependency", fmt("Import Dependency", get_value("import_dependency")))
    r1c2.metric("Domestic Supply", fmt("Domestic Supply", get_value("domestic_supply")))
    r2c1.metric("% Renewable Production", fmt("% Renewable Production", get_value("renew_prod_%")))
    r2c2.metric("% Non-Renewable Production", fmt("% Non-Renewable Production", get_value("no_renew_prod_%")))

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


)
with col1: st.plotly_chart(fig, use_container_width=True)

with col2: st.dataframe(summary, use_container_width=True)





