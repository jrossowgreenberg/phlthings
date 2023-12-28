from fastapi import FastAPI
from fastapi.responses import FileResponse
from phl_img import PhlImgModel
from phl_wthr import PhlWthrModel
from pydantic import BaseModel
import pendulum
import requests

mdl = PhlImgModel()
wthr = PhlWthrModel()

app = FastAPI()


class ImgRequestBody(BaseModel):
    prompt: str
    dalle_model: int = 3
    psychedelic: bool = True


@app.post("/img/generate", response_class=FileResponse)
async def generate(prompt: ImgRequestBody):
    timestamp = pendulum.now().timestamp()

    file_path = f"images/{timestamp}.png"

    if prompt.psychedelic:
        full_prompt = (
            "A landscape picture of Philadelphia that's kind of psychedelic includes the following description: "
            + prompt.prompt
        )
    else:
        full_prompt = (
            "A landscape picture of Philadelphia that includes the following description: "
            + prompt.prompt
        )

    image_url = mdl.generate(full_prompt, dalle_model=prompt.dalle_model)

    image = requests.get(image_url).content
    with open(file_path, "wb") as handler:
        handler.write(image)

    return file_path


@app.get("/wthr/forecast")
async def forecast():
    return wthr.get_forecast()
