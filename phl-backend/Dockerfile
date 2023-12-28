FROM python:3.11.7-bookworm

RUN pip install fastapi pendulum uvicorn openmeteo-requests pandas openai python-dotenv

WORKDIR /phlimg

RUN mkdir images

ADD main.py main.py
ADD phl_img.py phl_img.py
ADD phl_wthr.py phl_wthr.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
