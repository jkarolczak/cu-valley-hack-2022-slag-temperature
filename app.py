import streamlit as st
import pandas as pd
from numpy import genfromtxt
import plotly.express as px
import plotly.graph_objs
from time import sleep

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


st.title("Panel sterowania")


def draw_plot(time_window, step):
    fig = px.line(test_data.iloc[step:step + time_window], x="czas", y="temp", markers=True,
                  labels={
                     "czas": "Czas",
                     "temp": "Temperatura"
                 })
    fig.add_hline(y=1310, line_dash="dash", line_color="red")
    fig.update_layout(yaxis_range=[1280, 1320])
    plot.plotly_chart(fig, use_container_width=True)


test_data = pd.read_csv("resources/holdout.csv")
test_data.sort_values("czas", inplace=True)

time_window = st.slider("okno czasowe", min_value=3, max_value=100, value=15)

plot = st.empty()

for i in range(950):
    draw_plot(time_window, i)
    sleep(2)



with st.empty():
    for timestamp, temp in zip(test_data['czas'], test_data['temp']):
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        col1, col2, col3, col4 = st.columns(4)
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
        time.sleep(3)