

from openai import OpenAI
import os
#from dotenv import load_dotenv
import base64
import streamlit as st
import openai
from io import BytesIO
import tempfile
import os
import streamlit as st

# Create a function to transcribe audio using Whisper
def transcribe_audio(api_key, audio_file):
    openai.api_key = api_key
    with BytesIO(audio_file.read()) as audio_bytes:
        # Get the extension of the uploaded file
        file_extension = os.path.splitext(audio_file.name)[-1]
        
        # Create a temporary file with the uploaded audio data and the correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio_file:
            temp_audio_file.write(audio_bytes.read())
            temp_audio_file.seek(0)  # Move the file pointer to the beginning of the file
            
            # Transcribe the temporary audio file
            transcript = openai.Audio.translate("whisper-1", temp_audio_file)

    return transcript

api_key = st.secrets.openai_key
client = OpenAI(api_key=api_key)

def get_answer(messages):
    system_message = [{"role": "system", "content": "Your job is to help me fill out a form. This form is designed to understand the type of PowerPoint (PPT) you are submitting and other details so the responsible team can edit accordingly. If our conversation strays from the form, you'll guide it back gently to stay on task. You’ll be filling out a Workfront form, which will require the following details: PPT Title, Purpose of Presentation, Intended Audience for the PPT, Category of the PPT. Expect legnthy answers for questions about the purpose and be ready to give advice if needed. At the end getting all the information, list all the fields like this FIELD: USER INPUT in a list and confirm that everything looks okay.If the user confirms the informations is correct, output Submitted by -name of user-. If the user says something is wrong then correct the information and then reconfirm."}]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)
