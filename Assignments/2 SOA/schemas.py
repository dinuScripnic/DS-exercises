from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    Administrator = "Administrator"
    Secretary = "Secretary"
    Manager = "Manager"

    def __str__(self):
        return f"{self.value}"


class User(BaseModel):
    username: str
    password: str
    role: Role

    def __str__(self):
        return f"{self.username} {self.password} {self.role}"


class Login(BaseModel):
    username: str
    password: str

    def __str__(self):
        return f"{self.username} {self.password}"


class ChangeRole(BaseModel):
    username: str
    role: Role


class Status(str, Enum):
    Submitted = "Submitted"
    Processing = "Processing"
    Done = "Done"

    def __str__(self):
        return f"{self.value}"


class Job(BaseModel):
    id: str
    user: str
    timestamp: str
    status: Status
    date_range: str
    assets: list[int]

    def __str__(self):
        return f"{self.timestamp} {self.status} {self.date_range} {self.assets}"


class JobSubmit(BaseModel):
    date_range: str
    assets: list[int]

    def __str__(self):
        return f"{self.date_range} {self.assets}"


class ResultSubmit(BaseModel):
    job_id: str
    assets: list[float]

    def __str__(self):
        return f"{self.job_id} {self.assets}"


class Result(BaseModel):
    job_id: str
    timestamp: str
    assets: list[float]

    def __str__(self):
        return f"{self.job_id} {self.timestamp} {self.assets}"
