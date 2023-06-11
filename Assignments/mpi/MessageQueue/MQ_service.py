from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yaml
import requests
from schema import Message, Queue
from logs import write_log, create_log_file
from queue_functions import queues, check_exist, search_queue, delete_queue, QueueSaver


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

max_queue_size = config["queues_file"]["max_queue_size"]
creation_permission = config["creation_role"]
manipulation_permission = config["manipulation_role"]
port = config["port"]

qs = QueueSaver()


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["Options", "Get", "Post", "Put", "Delete"],
    allow_headers=["*"],
)


def get_user_role(token: str) -> list[str]:
    """
    Sends a request to the authentication service to get the user's role.

    Args:
        token (str): user's token

    Returns:
        list[str]: username and role
    """
    response = requests.get(
        url="http://localhost:8000/auth/role/?token=" + token
    ).content
    response = eval(response.decode("utf-8"))
    try:
        return response[0], response[1]
    except:
        write_log(f"Invalid token {token}", 403)
        raise HTTPException(status_code=403, detail="Invalid token")


@app.get("/queue/")
def get_queues(token: str) -> list[Queue]:
    username, role = get_user_role(token)
    if role not in manipulation_permission:
        write_log(f"User {username} tried to get all queues", 403)
        raise HTTPException(
            status_code=403, detail="You don't have permission to get all queues"
        )
    write_log(f"User {username} got all queues", 200)
    return queues


@app.get("/queue/{queue_id}")
def get_queue(token: str, queue_id: str) -> Queue:
    username, role = get_user_role(token)
    if role not in manipulation_permission:
        write_log(f"User {username} tried to get a queue", 403)
        raise HTTPException(
            status_code=403, detail="You don't have permission to get a queue"
        )
    # Check if the queue exists
    queue = search_queue(queue_id)
    if not queue:
        write_log(f"User {username} tried to get a queue that doesn't exist", 404)
        raise HTTPException(status_code=404, detail="The queue doesn't exist")
    write_log(f"User {username} got a queue {queue_id}", 200)
    return queue


@app.get("/queue/{queue_id}/size")
def get_queue_size(token: str, queue_id: str) -> str:
    username, role = get_user_role(token)
    if role not in manipulation_permission:
        write_log(f"User {username} tried to get a queue size", 403)
        raise HTTPException(
            status_code=403, detail="You don't have permission to get a queue size"
        )
    # Check if the queue exists
    queue = search_queue(queue_id)
    if not queue:
        write_log(f"User {username} tried to get a queue size that doesn't exist", 404)
        raise HTTPException(status_code=404, detail="The queue doesn't exist")
    write_log(f"User {username} got the queue size of {queue_id}", 200)
    return f"The size of the queue {queue_id} is {len(queue.queues)}"


@app.post("/queue/")
def create_queue(token: str, queue_id: str) -> Queue:
    user, role = get_user_role(token)
    if role not in creation_permission:
        write_log(f"User {user} tried to create a queue", 403)
        raise HTTPException(
            status_code=403, detail="You don't have permission to create a queue"
        )
    # Check if the queue already exists
    if check_exist(queue_id):
        write_log(f"User {user} tried to create a queue that already exists", 409)
        raise HTTPException(status_code=409, detail="The queue already exists")
    # Create the queue
    queue = Queue(queue_id=queue_id, max_size=max_queue_size, queues=[])
    queues.append(queue)
    # save the queue
    write_log(f"User {user} created a queue {queue_id}", 201)
    return queue


@app.delete("/queue/{queue_id}/delete")
def delete_q(token: str, queue_id: str) -> dict:
    user, role = get_user_role(token)
    if role not in creation_permission:
        write_log(f"User {user} tried to delete a queue", 403)
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete a queue"
        )
    # Check if the queue exists
    if not check_exist(queue_id):
        write_log(f"User {user} tried to delete a queue that doesn't exist", 404)
        raise HTTPException(status_code=404, detail="The queue doesn't exist")
    # Delete the queue
    delete_queue(queue_id)
    # save the log
    write_log(f"User {user} deleted a queue {queue_id}", 200)
    return {"message": f"Queue {queue_id} deleted successfully"}


@app.put("/queue/{queue_id}/push")
def push(token: str, queue_id: str, message: Message) -> dict:
    username, role = get_user_role(token)
    if role not in manipulation_permission:
        write_log(f"User {username} tried to push a message", 403)
        raise HTTPException(
            status_code=403, detail="You don't have permission to push a message"
        )
    # Check if the queue exists
    message = message.data
    if not check_exist(queue_id):
        write_log(
            f"User {username} tried to push a message to a queue that doesn't exist",
            404,
        )
        raise HTTPException(status_code=404, detail="The queue doesn't exist")
    # Check if the queue is full
    queue = search_queue(queue_id)

    if not queue:
        write_log(
            f"User {username} tried to push a message to a queue that doesn't exist",
            404,
        )
        raise HTTPException(status_code=404, detail="The queue doesn't exist")

    if len(queue.queues) == queue.max_size:
        write_log(f"User {username} tried to push a message to a full queue", 403)
        raise HTTPException(status_code=403, detail="The queue is full")
    # Push the message
    queue.queues.append(message)
    write_log(f"User {username} pushed a message to the queue {queue_id}", 201)
    return {"message": f"Message pushed successfully to queue {queue_id}"}


@app.put("/queue/{queue_id}/pull")
def pull(token: str, queue_id: str) -> dict:
    """
    Pull a message from the queue with the given id.

    Args:
        token (str): token of the user
        queue_id (str): id of the queue

    Raises:
        HTTPException: if the user doesn't have the permission to pull a message
        HTTPException: if the queue doesn't exist
        HTTPException: if the queue is empty

    Returns:
        _type_: the message pulled from the queue
    """
    username, role = get_user_role(token)
    if role not in manipulation_permission:
        write_log(f"User {username} tried to pull a message", 403)
        raise HTTPException(
            status_code=403, detail="You don't have permission to pull a message"
        )
    # Check if the queue exists
    queue = search_queue(queue_id)
    if not queue:  # if the queue doesn't exist
        write_log(
            f"User {username} tried to pull a message from a queue that doesn't exist",
            404,
        )
        raise HTTPException(status_code=404, detail="The queue doesn't exist")
    if len(queue.queues) == 0:  # if the queue is empty
        write_log(f"User {username} tried to pull a message from an empty queue", 403)
        raise HTTPException(status_code=403, detail="The queue is empty")
    # Pull the message
    message = queue.queues.pop(0)
    # save the log
    write_log(f"User {username} pulled a message from the queue {queue_id}", 200)
    # return the message
    return message


if __name__ == "__main__":
    import uvicorn

    create_log_file()
    qs.start()
    uvicorn.run(app, host="127.0.0.1", port=port)
