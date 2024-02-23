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

@st.cache_data(show_spinner=':blue[Loading survey data...]')
def load_cleaned_data():
    raw_data = utils.read_survey_data(cleaned_data_key)
    if 'cleaned_data' not in st.session_state:
        st.session_state['cleaned_data'] = raw_data
    return raw_data
df = load_cleaned_data()
# st.data_editor(df)

trial_columns = [column for column in df.columns[:3]]
# st.write(trial_columns)
# option = st.selectbox('pick a question', trial_columns)

@st.cache_data(show_spinner=':blue[Generating charts...]')
def generate_chart(chart_data, column):
    # chart_data = df.groupby(['Administrative Details/County',col]).size().reset_index(name='count')
    chart = px.bar(chart_data, x='Administrative Details/County', y='count', color=column, barmode='group', text_auto=True, width=500, height=400)
    chart.update_layout(showlegend=True, legend_title='', xaxis_title="",plot_bgcolor='whitesmoke', font_color='white')
    return chart

for column in trial_columns:
        split_column_name = column.split("/")[1]
        chart_data = df.groupby(['Administrative Details/County',column]).size().reset_index(name='count')

        # add df to session state
        if f"{split_column_name}_df" not in st.session_state:
            st.session_state[f"{split_column_name}_df"] = chart_data

        with st.container(border=True):         
            st.text(column.split("/")[1])
            with st.expander('Chart data'):
                edit_mode = st.checkbox('Edit mode', False, key=split_column_name)
                if edit_mode:
                     edited_df = st.data_editor(chart_data)
                     st.session_state[f"{split_column_name}_df"] = edited_df
                else:
                    unedited_df = st.dataframe(st.session_state[f"{split_column_name}_df"])

            chart_data_st = st.session_state[f"{split_column_name}_df"]
            chart = generate_chart(chart_data_st, column)       
            st.plotly_chart(chart, use_container_width=True)
            
