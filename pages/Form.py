import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
import pandas as pd 
from Login import email


#st.logo("jll.png")


st.title("Workfront Form Intake")
float_init()

st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

#st.sidebar.image("log.png", use_column_width=True)

user_data = {
    'email': ['medha@sample.com', 'hamza@sample.com', 'manu@sample.com', 'sara@sample.com', 'alex@sample.com'],
    'name': ['Medha Dandamudi', 'Hamza Rizvi', 'Manu Augustine', 'Sara Shah', 'Alex Kim'],
    'emp_id': ['AM112233', 'AS223344', 'AS123456', 'AW334455', 'AK556677'],
    'business_unit': ['Technology', 'Finance', 'Operations', 'Technology', 'Finance'],
    'business_line': ['Software Development', 'Financial Analysis', 'Supply Chain Management', 'Data Engineering', 'Risk Management'],
    'function': ['Development', 'Analysis', 'Logistics', 'Data Science', 'Compliance'],
    'market_code': ['US01', 'EU02', 'AP03', 'US01', 'EU02'],
    'account_code': ['ACC1001', 'ACC2002', 'ACC3003', 'ACC1001', 'ACC2002'],
    'project_code': ['PRJ5001', 'PRJ6002', 'PRJ7003', 'PRJ5001', 'PRJ6002']
}

df = pd.DataFrame(user_data)



email = st.session_state.email
user_info = df[df['email'] == email].iloc[0]

tab1, tab2 = st.tabs(["Manual Form Intake", "Voice-to-Text"]) 
with tab1:
    st.header("Form Intake")

    # Create a form
    with st.form("my_form"):
        name = st.text_input("Name", value=user_info['name'])
        email = st.text_input("Email", value=user_info['email'])
        emp_id = st.text_input("Employee ID", value=user_info['emp_id'])
        business_unit = st.text_input("Business Unit", value=user_info['business_unit'])
        business_line = st.text_input("Business Line", value=user_info['business_line'])
        function = st.text_input("Function", value=user_info['function'])
        market_code = st.text_input("Market Code", value=user_info['market_code'])
        account_code = st.text_input("Account Code", value=user_info['account_code'])
        project_code = st.text_input("Project Code", value=user_info['project_code'])

        title = st.text_area("Title of PPT")
        purpose = st.text_area("Purpose of Presentation")
        audience = st.text_area("Intended Audience")
        category = st.text_area("Category")

        
        # Submit button
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.success(f"Form submitted by {name}.")


user_info_str = f"""
Name: {user_info['name']}
Email: {user_info['email']}
Employee ID: {user_info['emp_id']}
Business Unit: {user_info['business_unit']}
Business Line: {user_info['business_line']}
Function: {user_info['function']}
Market Code: {user_info['market_code']}
Account Code: {user_info['account_code']}
Project Code: {user_info['project_code']}
"""


with tab2:





    def initialize_session_state():
        if "messages" not in st.session_state:
            st.session_state.messages = [
            {"role": "user", "content": f"Here is my information:\n{user_info_str}"},
            {"role": "assistant", "content": "Hello, I see that your information is already in the system. Can you provide me the title of your PPT?"}
        ]

    initialize_session_state()

    footer_container = st.container()
    with footer_container:
        
        audio_bytes = audio_recorder()

    


    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if audio_bytes:
        # Write the audio bytes to a file
        with st.spinner("Transcribing..."):
            webm_file_path = "temp_audio.mp3"
            with open(webm_file_path, "wb") as f:
                f.write(audio_bytes)

            transcript = speech_to_text(webm_file_path)
            if transcript:
                st.session_state.messages.append({"role": "user", "content": transcript})
                with st.chat_message("user"):
                    st.write(transcript)
                os.remove(webm_file_path)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                final_response = get_answer(st.session_state.messages)
            with st.spinner("Generating audio response..."):    
                audio_file = text_to_speech(final_response)
                autoplay_audio(audio_file)
            st.write(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            os.remove(audio_file)

    footer_container.float("bottom: 0rem;")
