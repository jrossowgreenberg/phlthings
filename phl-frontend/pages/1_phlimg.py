import streamlit as st
import requests
from io import BytesIO
import json


st.title("PHLimg")

# st.image("/Users/jrossowg/Documents/dev/best-of/phlimg-frontend/76ers.jpeg", width=250)

# col1, col2 = st.columns(2)


@st.cache_data
def generate_img(prompt: str, psych: bool):
    url = "http://phl-backend:8000/img/generate"
    body = {"prompt": prompt, "psychedelic": psych}
    r = requests.post(url, data=json.dumps(body))
    return BytesIO(r.content)


# Model Prompt
st.write("Type something...")
prompt = st.text_input("Type something...", key="prompt", label_visibility="collapsed")

# psychedelic Check box
psych = False
psych = st.checkbox("Make it trippy")


if st.button("Generate img"):
    if prompt and psych:
        st.image(generate_img(prompt=prompt, psych=True), caption=prompt)

    if prompt and not psych:
        st.image(generate_img(prompt=prompt, psych=False), caption=prompt)
