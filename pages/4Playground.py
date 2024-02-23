import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import plotly.express as px
from dotenv import load_dotenv
import utils
import os

load_dotenv()
cleaned_data_key = os.getenv('CLEANED_DATA')
raw_data_key = os.getenv('RAW_DATA')

st.title(':green[Build Your Own Charts]')
@st.cache_data(show_spinner=':blue[Loading survey data...]')
def load_cleaned_data():
    raw_data = utils.read_survey_data(cleaned_data_key)
    if 'cleaned_data' not in st.session_state:
        st.session_state['cleaned_data'] = raw_data
    return raw_data
df = load_cleaned_data()
# st.data_editor(df, num_rows='dynamic', hide_index=False)

columns = [column for column in df.columns]

c1,c2 = st.columns(2)
with c1:
    chart_columns = st.selectbox('Values', columns, index=None)
with c2:
    groupby_column = st.selectbox('Group by', columns, index=None)

if chart_columns:
    if groupby_column:
        try:
            chart_data = df.groupby([chart_columns,groupby_column]).size().reset_index(name='count')
            chart = px.bar(chart_data, x=groupby_column, y='count', color=chart_columns, barmode='group',text_auto=True, width=500, height=400)
            chart.update_layout(showlegend=True, legend_title='', xaxis_title="",plot_bgcolor='whitesmoke', font_color='white')
            st.plotly_chart(chart, use_container_width=True)

        except Exception as error:
            st.error(error)
    else:
        chart_data = df.groupby(chart_columns).size().reset_index(name='count')
        chart = px.bar(chart_data, x=chart_data.index, y='count', barmode='group',text_auto=True, width=500, height=400)   
        chart.update_layout(showlegend=True, legend_title='', xaxis_title="",plot_bgcolor='whitesmoke', font_color='white')
        st.plotly_chart(chart, use_container_width=True)

else:
    st.warning('Please select columns to visualize')


