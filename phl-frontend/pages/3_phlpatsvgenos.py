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


url = "http://phl-backend/yelp/reviews"
business_url = "http://phl-backend/yelp/businesses"


# Cachine functions
@st.cache_data(ttl=3600, max_entries=5)
def get_reviews(business_id):
    return requests.get(url + f"?business_id={business_id}")


@st.cache_data(ttl=3600, max_entries=5)
def get_business(business_id):
    return requests.get(business_url + f"/{business_id}")


# Reviews
pats_df = pd.DataFrame(get_reviews(business_id=pats_business_id).json()["reviews"])
genos_df = pd.DataFrame(get_reviews(business_id=genos_business_id).json()["reviews"])

# Business Info
pats_b = get_business(business_id=pats_business_id).json()
genos_b = get_business(business_id=genos_business_id).json()


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
