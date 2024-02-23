import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from authentication import auth
import plotly.express as px
from dotenv import load_dotenv
import os
import utils

st.set_page_config(
    page_title='K4R',
    layout='wide'
)
load_dotenv()
cleaned_data_key = os.getenv('CLEANED_DATA')


authenticator = auth.authenticate_user()
name, authentication_status, username = authenticator.login()
if authentication_status:
    c1,c2 = st.columns([.9,0.1])
    with c2:
        authenticator.logout('Logout', 'main')

    st.title(":green[Survey Analysis - K4RC]")

    @st.cache_data(show_spinner=':blue[Loading survey data...]')
    def load_cleaned_data():
        raw_data = utils.read_survey_data(cleaned_data_key)
        if 'cleaned_data' not in st.session_state:
            st.session_state['cleaned_data'] = raw_data
        return raw_data

    df = load_cleaned_data()
    group_names = [
            'Administrative Details',
            '1. General household questions',
            '2. Questions on the Outcomes of Women Empowerment Efforts ',
            '3. Questions on the Outcomes of Resilience Building Initiatives ',  
            '4. Questions on the Outcomes of Government Support to Communities',
            '5. Questions on Food Production',
            '6. Questions on recovery after environmental disasters',
            '7. Questions on Environmental Conservation and Management', 
            '8. QUESTIONS ON RESILIENCE',
            '9. Questions on Conflict-management and Peace-building',
            '10. Questions on Religion and Religious Freedom',
            '11. Questions on Triple Nexus',
            '12. QUESTIONS ON CROSS CUTTING ISSUES ', 
        ]
    quiz7_select_many =[
        "7. Questions on Environmental Conservation and Management/7.2 Which of the following are causing damage to the environment in your area?/Uncontrolled soil erosion",
        "7. Questions on Environmental Conservation and Management/7.2 Which of the following are causing damage to the environment in your area?/Overstocking",
        "7. Questions on Environmental Conservation and Management/7.2 Which of the following are causing damage to the environment in your area?/Overgrazing",
        "7. Questions on Environmental Conservation and Management/7.2 Which of the following are causing damage to the environment in your area?/Tree cutting",
        "7. Questions on Environmental Conservation and Management/7.2 Which of the following are causing damage to the environment in your area?/Other",
        "7. Questions on Environmental Conservation and Management/7.2 Others"
    ]

    option = st.selectbox('Survey questions', group_names)
    

    # @st.cache_data(show_spinner=':blue[Generating charts...]')
    # def generate_chart(col):
    #     if col == 'Administrative Details/County':
    #         chart_data = df[col].value_counts()
    #         chart = px.bar(chart_data, color=chart_data.index, text_auto=True, width=500, height=400)
    #         chart.update_layout(showlegend=True, legend_title='', xaxis_title="")
    #         return chart,chart_data

    #     chart_data = df.groupby(['Administrative Details/County',col]).size().reset_index(name='count')
    #     chart = px.bar(chart_data, x='Administrative Details/County', y='count', color=col,barmode='group', text_auto=True, width=500, height=400)
    #     chart.update_layout(showlegend=True, legend_title='', xaxis_title="",plot_bgcolor='whitesmoke', font_color='white')
    #     return chart,chart_data
    
    @st.cache_data(show_spinner=':blue[Generating charts...]')
    def generate_chart2(chart_data, column):
        chart = px.bar(chart_data, x='Administrative Details/County', y='count', color=column, barmode='group', text_auto=True, width=500, height=400)
        chart.update_layout(showlegend=True, legend_title='', xaxis_title="",plot_bgcolor=' #f0f3f4 ', font_color='white', bargap=0.3)
        return chart

    for column in df.columns:
        if option in column:
            split_column_name = column.split("/")[1]
            if column == 'Administrative Details/County':
                chart_data = df.groupby([column]).size().reset_index(name='count')
            else:
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
                chart = generate_chart2(chart_data_st, column)       
                st.plotly_chart(chart, use_container_width=True)
                


elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please login to view this page')