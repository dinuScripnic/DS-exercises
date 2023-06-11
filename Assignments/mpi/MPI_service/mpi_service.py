from mpi4py import MPI
import requests
import time
from timeseries import create_time_series, linear_fit, predict_value
from schema import Result
from datetime import datetime


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
scatter_tasks = None
auth_url = "http://localhost:8000/auth/login/"
queue_url = "http://localhost:7500/queue/"
admin = {"username": "admin", "password": "admin"}
timeseries = create_time_series(100, 300)

if rank == 0:
    token = requests.post(url=auth_url, json=admin).content
    # decode and get the token
    token = eval(token.decode("utf-8"))["token"]


while True:
    try:
        if rank == 0:
            pull_response = None
            while pull_response is None:
                pull_response = requests.put(
                    queue_url + "queue_job/pull", params={"token": token}
                ).json()
                if "detail" in pull_response.keys():
                    print(pull_response["detail"])
                    time.sleep(3)
                    pull_response = None

            id = pull_response["id"]
            user = pull_response["user"]
            assets = pull_response["assets"]
            scatter_tasks = [None] * size
            current_proc = 0
            for asset in assets:
                if scatter_tasks[current_proc] is None:
                    scatter_tasks[current_proc] = []
                scatter_tasks[current_proc].append(int(asset))
                current_proc = (current_proc + 1) % size
        else:
            tasks = None
        assets_to_process = comm.scatter(scatter_tasks, root=0)
        calcs = []
        if assets_to_process is not None:
            for asset in assets_to_process:
                model = linear_fit(timeseries[asset])
                predict = predict_value(model, 301)
                calcs.append(predict)
        result = comm.gather(calcs, root=0)
        if comm.rank == 0:
            print("Gathered results for job_id: ", id)
            result = result[0]
            average = sum(result) / len(result)
            result = Result(
                job_id=id,
                timestamp=str(datetime.now()),
                assets=float(average[0]),
            )
            requests.put(
                queue_url + "queue_result/push",
                params={"token": token},
                json={"data": result.__dict__},
            )
    except Exception as e:
        print(e)
        quit()
