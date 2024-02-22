import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
from dotenv import load_dotenv
load_dotenv()

def authenticate_user():
    pss_username = os.getenv('PSS_USERNAME')
    pss_name = os.getenv('PSS_NAME')
    pss_password = os.getenv('PSS_PASSWORD')

    k4r_username = os.getenv('K4R_USERNAME')
    k4r_name = os.getenv('K4R_NAME')
    k4r_password = os.getenv('K4R_PASSWORD')

    cookie_expiry_days = os.getenv('COOKIE_EXPIRY_DAYS')
    cookie_key = os.getenv('COOKIE_KEY')
    cookie_name = os.getenv('COOKIE_NAME')

    config = {
        "credentials": {
            "usernames": {
                pss_username: {"name": pss_name,"password": pss_password},
                k4r_username: {"name": k4r_name,"password": k4r_password}
            }
        },
        "cookie": {
            "expiry_days": cookie_expiry_days,
            "key": cookie_key,
            "name": cookie_name
        }
    }
    
    authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
        )
    return authenticator
