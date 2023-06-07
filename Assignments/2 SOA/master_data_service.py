from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer
import json
import datetime
from schemas import Job, Result, JobSubmit, ResultSubmit, Status
from auth import AuthHandler
from fastapi.middleware.cors import CORSMiddleware
import requests


app = FastAPI()
security = HTTPBearer()
authHandler = AuthHandler()

allowed_roles = ["Administrator", "Manager"]
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_if_file_exists(filename: str) -> bool:
    """
    Check if the file exists

    Args:
        filename (str): file to check

    Returns:
        bool: True if file exists, False otherwise
    """
    try:  # try to open file
        with open(filename, "r") as f:
            return True
    except FileNotFoundError:  # if file does not exist
        return False


def get_data_from_file(filename: str) -> list:
    """
    Opens the database file and returns the data.
    If the database file does not exist, it returns an empty list.

    Args:
        filename (str): database file

    Returns:
        list: data from the database file
    """
    if check_if_file_exists(filename):  # check if file exists
        with open(filename, "r") as f:  # open file
            return json.load(f)  # return data
    else:  # if file does not exist
        return []  # return empty list


def write_data_to_file(filename: str, data: list) -> None:
    with open(filename, "w") as f:
        json.dump(data, f)


def get_user_role(token: str) -> str:
    response = requests.get(
        url="http://localhost:8000/auth/role/?token=" + token
    ).content
    response = eval(response.decode("utf-8"))
    role = response[1]
    username = response[0]
    return username, role


@app.post("/master/job/")
async def create_job(token: str, job: JobSubmit) -> str:
    """
    Creates a new job and returns the job id.

    Args:
        token (str): token used for authentication
        job (JobSubmit): job data to be submitted, contains date_range and assets

    Raises:
        HTTPException: in case of invalid asset value
        HTTPException: in case the user is not allowed to submit jobs

    Returns:
        str: job id of the submitted job
    """
    username, role = get_user_role(token)
    if role in allowed_roles:
        for a in job.assets:
            # check if asser > 100 or < 0 and int
            if not isinstance(a, int) or a > 100 or a < 0:
                raise HTTPException(status_code=400, detail="Invalid asset value")
        timestamp = datetime.datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        data = get_data_from_file("jobs.json")
        job = Job(
            id=f"job_{len(data)}",
            user=username,
            timestamp=timestamp,
            status=Status.Submitted,
            date_range=job.date_range,
            assets=job.assets,
        )
        data.append(job.__dict__)
        write_data_to_file("jobs.json", data)
        return job.id
    else:
        raise HTTPException(status_code=403, detail="Not allowed")


@app.get("/master/jobs/")
async def get_jobs(token: str) -> list:
    """
    Returns a list of all jobs in the database.
    If the database file does not exist, it returns an empty list.

    Args:
        token (str): authentication token

    Raises:
        HTTPException: if the user is not allowed to get jobs

    Returns:
        list: list of all jobs with folowing attributes: id, user, timestamp, status, date_range, assets
    """
    if get_user_role(token)[1] in allowed_roles:
        return get_data_from_file("jobs.json")
    else:
        raise HTTPException(status_code=403, detail="Not allowed")


@app.put("/master/job/{job_id}/")
async def update_job(token: str, job_id: str) -> int:
    """


    Args:
        token (str): authentication token
        job_id (str): job id to be updated

    Raises:
        HTTPException: if the job database does not exist
        HTTPException: if the job with the given id does not exist
        HTTPException: if user is not allowed to update jobs

    Returns:
        int: _description_
    """
    if get_user_role(token)[1] in allowed_roles:
        jobs = get_data_from_file("jobs.json")
        if not jobs:
            raise HTTPException(status_code=404, detail="Jobs database not found")
        if job_id not in [job["id"] for job in jobs]:
            raise HTTPException(status_code=404, detail="Job not found")
        for job in jobs:
            if job["id"] == job_id:
                job["status"] = Status.Processing
        write_data_to_file("jobs.json", jobs)
        return 200
    else:
        raise HTTPException(status_code=403, detail="Not allowed")


@app.get("/master/results/")
async def get_results(token: str) -> list:
    """
    Returns a list of all results in the database.
    If the database file does not exist, it returns an empty list.

    Args:
        token (str): authentication token

    Raises:
        HTTPException: if the user is not allowed to get results

    Returns:
        list: list of all results with folowing attributes: job_id, timestamp and assets
    """
    # username = authHandler.decode_token(token)
    if get_user_role(token)[1] in allowed_roles:
        return get_data_from_file("results.json")
    else:
        raise HTTPException(status_code=403, detail="Not allowed")


@app.post("/master/result/")
async def create_result(token: str, result: ResultSubmit) -> str:
    """


    Args:
        token (str): authentication token
        result (ResultSubmit): result data to be submitted, contains job_id and assets

    Raises:
        HTTPException: if the job is already in the database
        HTTPException: if the job with the given id does not exist
        HTTPException: if the job is already done
        HTTPException: if the number of assets is not equal to the number of assets in the job
        HTTPException: if the user is not allowed to submit results

    Returns:
        str: job id of the finished job
    """
    if get_user_role(token)[1] in allowed_roles:
        data = get_data_from_file("jobs.json")
        job = [job for job in data if job["id"] == result.job_id]
        if len(job) > 1:
            raise HTTPException(status_code=401, detail="Job already in database")
        job = job[0]
        assert_len = len(job["assets"])
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        if job["status"] == Status.Done:
            raise HTTPException(status_code=400, detail="Job already done")
        assert_len = len(job["assets"])
        if len(result.assets) != assert_len:
            raise HTTPException(status_code=400, detail="Wrong number of assets")
        job["status"] = Status.Done
        write_data_to_file("jobs.json", data)
        data = get_data_from_file("results.json")
        timestamp = datetime.datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        result = Result(job_id=result.job_id, assets=result.assets, timestamp=timestamp)
        data.append(result.__dict__)
        write_data_to_file("results.json", data)
        return result.job_id
    else:
        raise HTTPException(status_code=403, detail="Not allowed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
