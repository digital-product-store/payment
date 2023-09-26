#!/usr/bin/env python3

import os
import uuid
import random

from elasticapm.contrib.starlette import ElasticAPM, make_apm_client

from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel


ELASTIC_APM_URL = os.getenv("ELASTIC_APM_URL", "http://localhost:8200")

app = FastAPI()
apm = make_apm_client(
    {
        "SERVICE_NAME": "payment",
        "SERVER_URL": ELASTIC_APM_URL,
        "CAPTURE_HEADERS": True,
        "CAPTURE_BODY": "all",
    }
)
app.add_middleware(ElasticAPM, client=apm)


@app.get("/_health")
async def health_check():
    return Response(status_code=200)


class Payment(BaseModel):
    amount: float
    currency: str
    card_number: str
    exp_date: str
    cvv: str


class Paid(BaseModel):
    id: str


@app.post("/_private/api/v1/payment")
async def do_payment(payment: Payment) -> Paid:
    if payment.cvv == "666":
        return Response(status_code=503)

    if payment.cvv == "777" and int(random.random() * 100) % 3 == 0:
        return Response(status_code=408)

    return Paid(id=str(uuid.uuid4()))
