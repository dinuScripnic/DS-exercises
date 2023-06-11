from __future__ import annotations

import requests
from schema import Job, Status, Result
from datetime import datetime
from random import randint

auth_url = "http://localhost:8000/auth/login/"
admin = {"username": "admin", "password": "admin"}
token = requests.post(url=auth_url, json=admin).content
# decode and get the token
token = eval(token.decode("utf-8"))["token"]

for i in range(5):
    job = Job(
        id="job" + str(i),
        user="admin",
        status=Status.Submitted,
        timestamp=str(datetime.now()),
        date_range="2021-01-01 00:00:00 - 2021-01-01 23:59:59",
        assets=[randint(0, 99) for _ in range(randint(5, 20))],
    )
    job_request = requests.put(
        url="http://localhost:7500/queue/queue_job/push",
        params={"token": token},
        json={"data": job.__dict__},
    )
