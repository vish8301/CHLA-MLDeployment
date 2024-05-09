# Dockerfile

FROM python:3.8

COPY requirements.txt frontend/requirements.txt

WORKDIR /frontend

RUN pip install -r requirements.txt

COPY . /frontend

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]
CMD ["user_inputs.py"]