FROM python:3.10-alpine

WORKDIR /opt/payment

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/main.py .

USER nobody:nobody

CMD uvicorn main:app --host 0.0.0.0
