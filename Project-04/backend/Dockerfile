# Dockerfile

FROM python:3.8

COPY requirements.txt backend/requirements.txt

WORKDIR /backend

RUN pip install -r requirements.txt

COPY . /backend

EXPOSE 8000

CMD ["uvicorn", "prediction:app", "--host", "0.0.0.0", "--port", "8000" , "--reload"]