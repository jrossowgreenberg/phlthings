FROM python:3.11.7-bookworm

RUN pip install streamlit pandas pendulum

WORKDIR /phl

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "home.py"]
