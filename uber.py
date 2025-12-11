import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber Pickups in NYC")

DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

date_column = 'date/time'
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows= nrows)
    lowrcase = lambda x: str(x).lower()
    data.rename(lowrcase, axis='columns', inplace= True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    
data_load_state = st.text("Data Loading...")
data=load_data(10000)
data_load_state.text("Done!")
