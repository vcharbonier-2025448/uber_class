import streamlit as st
import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')
import hvplot.pandas
idf = df.interactive()

df = pd.read_csv("ireland_energy.csv")

st.title("Ireland Energy")

year_slider = pn.widgets.IntSlider(name='Year slider', start=2000, end=2023, step=5, value=2023)
year_slider

# Radio buttons for ratios
yaxis_ratio = pn.widgets.RadioButtonGroup(
    name='Y axis', 
    options=['import_dependency', 'domestic_supply',],
    button_type='success'
)
yaxis_ratio

energy_pipeline = (
    idf[
        (idf.year <= year_slider)&
        (idf.country.isin(["Ireland", "Uruguay"]))
    ]
    .groupby(['country', 'year'])[yaxis_ratio].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='year')  
    .reset_index(drop=True)
)
energy_pipeline
