import string
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
import plotly.express as px
import plotly.graph_objs
from time import sleep
import xgboost
import pickle
import shap
import streamlit.components.v1 as components
from PIL import Image

# import warnings
# warnings.filterwarnings('ignore') # https://github.com/streamlit/streamlit/issues/1430
import time
from datetime import datetime
import warnings

# warnings.filterwarnings('ignore') # https://github.com/streamlit/streamlit/issues/1430

# csv_file = st.file_uploader(label="Wprowadź dane")
# if csv_file:
#     if not csv_file.name.endswith(".csv"):
#         st.error("Proszę wprowadzić plik z rozszerzeniem csv")
#     else:

favicon = Image.open('resources/coin.png')
st.set_page_config(
        page_title="Miedź na oku",
        page_icon=favicon,
        layout="wide",
        # initial_sidebar_state="expanded"
    )


test_data = pd.read_csv("resources/holdout.csv")
test_data.sort_values("czas", inplace=True)

model = pickle.load(open("resources/cuv-62.pkl", 'rb'))
explainer = shap.Explainer(model)
# model_data = test_data.drop(["czas", "temp"], axis=1)
# shap_values = explainer(model_data)

st.title("Panel kontrolny")

def draw_plot(plot, time_window, step):
    fig = px.line(test_data.iloc[max(step-time_window, 0):step+1], x="czas", y="temp", markers=True,
                  labels={
                     "czas": "Czas",
                     "temp": "Temperatura"
                 })
    fig.add_hline(y=1310, line_dash="dash", line_color="red")
    fig.update_layout(yaxis_range=[1280, 1320])
    plot.plotly_chart(fig, use_container_width=True)

def draw_shap(shap_values):
    shap_plot = shap.plots.force(shap_values[0])
    shap_html = f"<head>{shap.getjs()}</head><body>{shap_plot.html()}</body>"
    components.html(shap_html)

def xlsx_to_dict(filename: str) -> dict:
    df = pd.read_table(filename)
    return dict(zip(df.Tagname.str.lower(), df.opis))

def parse_columns(df: pd.DataFrame) -> pd.DataFrame:
    new_cols = {}
    for col in df.columns:
        new_cols[col] = col.split("_", 1)[0]
    df = df.rename(columns=new_cols)
    tagnames = xlsx_to_dict('resources/nametags.txt')
    df = df.rename(columns=tagnames)
    return df

container = st.empty()
time_window = st.slider("Przedział pobierania pomiarów w minutach", min_value=3, max_value=100, value=15)
container_3 = st.empty()
plot = st.empty()
container_2 = st.empty()

for i, row in test_data.iterrows():
    with container.empty():
        col1, col2, col3, col4 = container.columns(4)
        temp = row['temp']
        timestamp = datetime.strptime(row['czas'], '%Y-%m-%d %H:%M:%S')
        model_input = pd.DataFrame(row.drop(["czas", "temp"]), dtype=np.float64).transpose()

        model_input = parse_columns(model_input)

        col1.metric("Data", timestamp.strftime('%d/%m/%y'))
        col2.metric("Czas", timestamp.strftime('%H:%M'))

        if "last_temp" in locals():
            col3.metric("Temperatura", f'{temp} °C', f'{temp - last_temp} °C', delta_color='off')
        else:
            col3.metric("Temperatura", f'{temp} °C')
        if int(temp) > 1310:
            col4.metric("", "⚠️")
        else:
            col4.metric("", "✅")
        last_temp = temp

        test_data.at[i, "temp"] = model.predict(model_input)
        draw_plot(plot, time_window, i)

    with container_2.empty():
        shap_values = explainer(model_input)
        draw_shap(shap_values)    
        time.sleep(5)