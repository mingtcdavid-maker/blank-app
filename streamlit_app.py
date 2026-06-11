import streamlit as st
import requests
import json


st.title("Demo for livetranslate")
st.write(
    "Record audio below and let the app translate:"
)

st.audio_input("Click to record")

