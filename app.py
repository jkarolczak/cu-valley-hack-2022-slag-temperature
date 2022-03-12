import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap
import time

import streamlit.components.v1 as components
import plotly.express as px

from datetime import datetime
from PIL import Image

if 'time' not in st.session_state:  # monitor time change
    st.session_state['time'] = 0

favicon = Image.open('static/coin.png')
st.set_page_config(
    page_title="Miedź na oku",
    page_icon=favicon,
    layout="wide",
    # initial_sidebar_state="expanded"
)

test_data = pd.read_csv("static/mockup_data.csv")

model = pickle.load(open("static/model.pkl", 'rb'))
explainer = shap.Explainer(model)

for i, row in test_data[:30].iterrows():  # calculate temp for the first 30 minutes
    model_input = pd.DataFrame(row.drop(["czas", "temp"]), dtype=np.float64).transpose()
    temp = np.round(model.predict(model_input)[0])
    test_data.at[i, "temp"] = temp


def draw_plot(plot, time_window, step):
    fig = px.line(test_data.iloc[max(step - time_window, 0):step + 1], x="czas", y="temp", markers=True,
                  labels={
                      "czas": "Czas",
                      "temp": "Temperatura"
                  })
    fig.add_hline(y=1310, line_dash="dash", line_color="red")
    fig.update_layout(yaxis_range=[1290, 1315])
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
    tagnames = xlsx_to_dict('static/nametags.txt')
    df = df.rename(columns=tagnames)
    return df


st.title("Panel kontrolny")

container = st.empty()

time_window = st.slider("Przedział pobierania pomiarów w minutach", min_value=3, max_value=60, value=30)

st.write('Temperatura żużlu wewnątrz pieca zawiesinowego Huty Miedzi KGHM "Głogów II"')

plot = st.empty()

st.write('Wpływ parametrów na temperaturę')
container_shap = st.empty()

for i, row in test_data[30 + (st.session_state.time) % 29:].iterrows():
    st.session_state.time += 1
    with container.empty():
        col1, col2, col3, col4 = container.columns(4)
        timestamp = datetime.strptime(row['czas'], '%Y-%m-%d %H:%M:%S')
        model_input = pd.DataFrame(row.drop(["czas", "temp"]), dtype=np.float64).transpose()

        model_input = parse_columns(model_input)

        temp = np.round(model.predict(model_input)[0])
        test_data.at[i, "temp"] = temp

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

        draw_plot(plot, time_window, i)

    with container_shap.empty():
        shap_values = explainer(model_input)
        draw_shap(shap_values)
        time.sleep(5)
