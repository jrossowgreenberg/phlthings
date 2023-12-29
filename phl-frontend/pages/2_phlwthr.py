import streamlit as st
import requests
import pandas as pd
import pendulum


st.title("PHLwthr")


url = "http://phl-backend:8000/wthr/forecast"
r = requests.get(url)
df = pd.DataFrame(r.json())

st.write("Today's forecast...")

today = df.iloc[0]
header = pendulum.parse(today["date"]).format("MMMM D, YYYY")

today["high ⬆️"] = int(today["temp_high"])
today["low ⬇️"] = int(today["temp_low"])
today["sunrise 🌅"] = today["sunrise"]
today["sunset 🌇"] = today["sunset"]

today_df = today[["high ⬆️", "low ⬇️", "sunrise 🌅", "sunset 🌇"]]
today_df.rename(header, inplace=True)

st.write(today_df)


st.write("7-day high and low temps...")

st.line_chart(df, x="date", y=["temp_high", "temp_low"])

st.write("7-day sunrise and sunset...")

st.write(df[["date", "sunrise", "sunset"]])
