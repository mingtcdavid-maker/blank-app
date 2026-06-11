import streamlit as st
import requests
import json


st.title("Demo for livetranslate")
st.write(
    "Record audio below and let the app translate:"
)



language_from = st.selectbox("Select language inputted.", 
                             [
                                 "singlish",
                                 "chinese",
                                 "indonesian",
                                 "malay",
                                 "filipino",
                                 "hindi",
                                 "tamil"
                             ])


language_to = st.selectbox("Select language you wish to translate to.", 
                             [
                                 "singlish",
                                 "chinese",
                                 "indonesian",
                                 "malay",
                                 "filipino",
                                 "hindi",
                                 "tamil"
                             ])

audio = st.audio_input("Click to record")


if audio:
    st.write("Generating response, please wait for 30 seconds.")

    valsea_response = requests.post(
        "https://api.valsea.ai/v1/audio/transcriptions",
        headers={"Authorization": st.secrets["VALSEA_KEY"]},
        files={"file": ("audio.wav", audio, "audio/wav")},
        data={
            "model": "valsea-transcribe",
            "language": language_from,
            "response_format": "verbose_json",
        },)



    chatgpt_response = requests.post(
            url = "https://openrouter.ai/api/v1/chat/completions",
            headers = {"Authorization": st.secrets["OPENROUTER_KEY"]},
            json = {"model": "openai/gpt-5.2",
                    "messages": [
                    {"role": "system", "content": "You are an assistant for SCDF officers responding to live incidents. You are to help translate between the given languages. Do generate the text as plain text."},
                    {"role": "user", "content": f"{valsea_response.json()} is the user input, it is in {language_from}. Please translate it to {language_to}"}
                    ]})

    st.write(valsea_response.json()["text"])

    st.write(chatgpt_response.json()["choices"][0]["message"]["content"])