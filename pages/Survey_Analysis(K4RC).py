import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from authentication import auth
import plotly.express as px

st.set_page_config(
    page_title='K4R',
    layout='wide'
)

authenticator = auth.authenticate_user()
name, authentication_status, username = authenticator.login()
if authentication_status:
    c1,c2 = st.columns([.9,0.1])
    with c2:
        authenticator.logout('Logout', 'main')

    st.title(":green[Survey Analysis - K4RC]")

    @st.cache_data(show_spinner=':blue[Loading survey data...]')
    def load_data():
        df = pd.read_excel('cleaned_data.xlsx')
        return df

    df = load_data()
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

    @st.cache_data(show_spinner=':blue[Generating charts...]')
    def generate_chart(col):
        chart_data = df[col].value_counts()
        chart = px.bar(chart_data, color=chart_data.index, title=col.split("/")[1], text_auto=True)
        chart.update_layout(
            showlegend=False,
            xaxis_title="",
        )
        return chart
    
    for name in group_names:
        with st.expander(name, expanded=False):
            for col in df.columns:
                if name in col:
                    chart = generate_chart(col)
                    st.plotly_chart(chart)

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please login to view this page')