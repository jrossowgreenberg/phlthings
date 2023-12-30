import streamlit as st
import requests
import pandas as pd
import pendulum

st.set_page_config(layout="wide")
st.title("PHLPatsVGenos")

col1, col2 = st.columns(2)

pats_business_id = "PP3BBaVxZLcJU54uP_wL6Q"
genos_business_id = "IkY2ticzHEn4QFn8hQLSWg"


def star_emoji_gen(star_num: int):
    star = "⭐"
    black_star = "★"

    black_stars = 5 - star_num

    stars = [star for s in range(star_num)]
    not_stars = [black_star for s in range(black_stars)]
    result = stars + not_stars
    return "".join(result)


url = "http://127.0.0.1:8000/yelp/reviews"
business_url = "http://127.0.0.1:8000/yelp/businesses"

# Reviews
pats = requests.get(url + f"?business_id={pats_business_id}")
pats_df = pd.DataFrame(pats.json()["reviews"])
genos = requests.get(url + f"?business_id={genos_business_id}")
genos_df = pd.DataFrame(genos.json()["reviews"])

# Business Info
pats_b = requests.get(business_url + f"/{pats_business_id}").json()
genos_b = requests.get(business_url + f"/{genos_business_id}").json()


with col1:
    st.text("Pat's King of Steaks")
    st.image("images/pats.jpg")
    st.write(f"""Review Count: {pats_b["review_count"]}""")
    st.write(f"""Overall Rating: {"%g" % pats_b["rating"]}/5""")

    st.write("___\nMost Recent Reviews: ")

    for index, row in pats_df.iterrows():
        time_created = row["time_created"]
        rating = row["rating"]
        text = row["text"]
        url = row["url"]
        time_created = pendulum.parse(row["time_created"]).format("MMMM DD, YYYY")

        star_rating = star_emoji_gen(rating)
        st.write(star_rating)
        st.write(time_created)
        st.write(text)
        st.write(f"[full review]({url})")
        st.write("___")

with col2:
    st.text("Geno's Steaks")
    st.image("images/genos.jpg")
    st.write(f"""Review Count: {genos_b["review_count"]}""")
    st.write(f"""Overall Rating: {"%g" % genos_b["rating"]}/5""")

    st.write("___\nMost Recent Reviews: ")

    for index, row in genos_df.iterrows():
        time_created = row["time_created"]
        rating = row["rating"]
        text = row["text"]
        url = row["url"]

        star_rating = star_emoji_gen(rating)
        st.write(star_rating)
        st.write(text)
        st.write(f"[full review]({url})")
        st.write("___")
