
import streamlit as st
import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import pandas as pd


st.set_page_config(page_title="JLL Workfront", layout="wide")
float_init()

#st.logo("jll.png")

st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("Workfront Form Intake")



credentials = {
    "medha@sample.com": "medha1",
    "hamza@sample.com": "hamza1",
    "manu@sample.com": "manu1"
}


# Create an empty container
placeholder = st.empty()

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your credentials")
    email = st.text_input("Email")
    st.session_state.email = email
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")
    

if submit and email in credentials and credentials[email] == password:
    placeholder.empty()
    st.success("Login successful")
    st.switch_page("pages/Form.py")
elif submit and email not in credentials and password != credentials[email]:
     st.error("Login failed")



