import streamlit as st
import requests
import json


st.title("Demo for livetranslate")
st.write(
    "Record audio below and let the app translate:"
)
audio = st.audio_input("Click to record")


if audio:
    st.write("Generating response, please wait for 30 seconds.")

    valsea_response = requests.post(
        "https://api.valsea.ai/v1/audio/transcriptions",
        headers={"Authorization": st.secrets["VALSEA_KEY"]},
        files={"file": ("audio.wav", audio, "audio/wav")},
        data={
            "model": "valsea-transcribe",
            "language": "malay",
            "response_format": "verbose_json",
        },)



    chatgpt_response = requests.post(
            url = "https://openrouter.ai/api/v1/chat/completions",
            headers = {"Authorization": st.secrets["OPENROUTER_KEY"]},
            json = {"model": "openai/gpt-5.2",
                    "messages": [
                    {"role": "system", "content": "You are an assistant for SCDF officers responding to live incidents. You are to help translate between the given language and chinese. Do generate the text as plain text."},
                    {"role": "user", "content": f"{valsea_response.json()} is the user input."}
                    ]})

    st.write(valsea_response.json()["text"])

    st.write(chatgpt_response.json()["choices"][0]["message"]["content"])