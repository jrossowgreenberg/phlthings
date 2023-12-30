import streamlit as st
import requests
from io import BytesIO
import json
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.title("PHLimg")

with open("auth.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

name, authentication_status, username = authenticator.login("Login", "sidebar")

if authentication_status:
    authenticator.logout("Logout", "sidebar")

    @st.cache_data
    def generate_img(prompt: str, psych: bool):
        url = "http://phl-backend:8000/img/generate"
        body = {"prompt": prompt, "psychedelic": psych}
        r = requests.post(url, data=json.dumps(body))
        return BytesIO(r.content)

    # Model Prompt
    st.write("Type something...")
    prompt = st.text_input(
        "Type something...", key="prompt", label_visibility="collapsed"
    )

    # psychedelic Check box
    psych = False
    psych = st.checkbox("Make it trippy")

    if st.button("Generate img"):
        if prompt and psych:
            st.image(generate_img(prompt=prompt, psych=True), caption=prompt)

        if prompt and not psych:
            st.image(generate_img(prompt=prompt, psych=False), caption=prompt)

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
