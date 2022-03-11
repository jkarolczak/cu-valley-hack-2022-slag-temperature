import streamlit as st
import pandas as pd
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