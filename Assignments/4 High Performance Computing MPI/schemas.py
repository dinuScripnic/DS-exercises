from pydantic import BaseModel
from enum import Enum

def __init__():
    pass

class Role(str, Enum):
    Administrator = "Administrator"
    Secretary = "Secretary"
    Manager = "Manager"

    def __str__(self):
        return f"{self.value}"


class Status(str, Enum):
    Submitted = "Submitted"
    Processing = "Processing"
    Done = "Done"

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

    def __str__(self):
        return f"{self.username} {self.role}"


class Job(BaseModel):
    id: str
    user: str
    timestamp: str
    status: Status
    date_range: str
    assets: list[int]

    def __str__(self):
        return f"{self.timestamp} {self.status} {self.date_range} {self.assets}"


class Result(BaseModel):
    job_id: str
    timestamp: str
    assets: list[float]

    def __str__(self):
        return f"{self.job_id} {self.timestamp} {self.assets}"


class Push(BaseModel):  # not sure i need this
    queue_id: str
    search_id: str

    def __str__(self):
        return f"{self.queue_id} {self.search_id}"    


class Message(BaseModel):
    data: dict
    
    
class Queue(BaseModel):
    queue_id:str
    max_size:int
    queues:list[Message]

    def __str__(self):
        return f"{self.queue_id} {self.max_size} {self.queues}"
