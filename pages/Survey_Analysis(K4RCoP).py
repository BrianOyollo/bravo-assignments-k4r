import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv
pss_name = os.getenv('PSS_NAME')

st.title(":green[Survey Analysis - K4R CoP]")
st.write('checking')
st.write(pss_name)
