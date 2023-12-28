from openai import OpenAI
from dotenv import load_dotenv
import os
import requests


class PhlImgModel:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def generate(self, prompt, dalle_model: int = 3):
        if dalle_model == 3:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                style="vivid",
                quality="standard",
                n=1,
            )
        elif dalle_model == 2:
            response = self.client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size="256x256",
                style="vivid",
                quality="standard",
                n=1,
            )
        return response.data[0].url
