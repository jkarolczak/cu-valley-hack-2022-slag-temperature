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

# import warnings
# warnings.filterwarnings('ignore') # https://github.com/streamlit/streamlit/issues/1430
import time
from datetime import datetime
import warnings

#warnings.filterwarnings('ignore') # https://github.com/streamlit/streamlit/issues/1430

# csv_file = st.file_uploader(label="Wprowadź dane")
# if csv_file:
#     if not csv_file.name.endswith(".csv"):
#         st.error("Proszę wprowadzić plik z rozszerzeniem csv")
#     else:


test_data = pd.read_csv("resources/holdout.csv")
test_data.sort_values("czas", inplace=True)

model = pickle.load(open("resources/cuv-62.pkl", 'rb'))
explainer = shap.Explainer(model)
# model_data = test_data.drop(["czas", "temp"], axis=1)
# shap_values = explainer(model_data)

st.title("Panel sterowania")


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



container = st.empty()

plot = st.empty()
time_window = st.slider("Okno czasowe", min_value=3, max_value=100, value=15)

with container.empty():
    for i, row in test_data.iterrows():
        col1, col2, col3, col4 = container.columns(4)
        temp = row['temp']
        timestamp = datetime.strptime(row['czas'], '%Y-%m-%d %H:%M:%S')
        model_input = pd.DataFrame(row.drop(["czas", "temp"]), dtype=np.float64).transpose()

        col1.metric("Data", timestamp.strftime('%d/%m/%y'))
        col2.metric("Czas", timestamp.strftime('%H:%M'))

        if "last_temp" in locals():
            col3.metric("Temperatura", f'{temp} °C', f'{temp - last_temp} °C', delta_color='off')
        else:
            col3.metric("Temperatura", f'{temp} °C')
        if int(temp) > 1310:
            col4.metric("", "❌")
        else:
            col4.metric("", "✅")
        last_temp = temp

        test_data.at[i, "temp"] = model.predict(model_input)

        shap_values = explainer(model_input)
        draw_shap(shap_values)

        draw_plot(plot, time_window, i)
        time.sleep(5)


