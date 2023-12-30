import requests
import os


class PhlYelp:
    def __init__(self):
        yelp_api_key = os.environ.get("YELP_API_KEY")

        self.default_headers = {"Authorization": f"Bearer {yelp_api_key}"}

    def get_reviews(self, business_id: str):
        url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews?limit=20&sort_by=newest"

        response = requests.get(url, headers=self.default_headers)

        return response.json()

    def get_business(self, business_id: str):
        url = f"https://api.yelp.com/v3/businesses/{business_id}"

        response = requests.get(url, headers=self.default_headers)

        print(response.json())

        return response.json()
