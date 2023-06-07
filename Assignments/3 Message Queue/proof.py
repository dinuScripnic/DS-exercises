# this is the proof of the assignment 3

# from auth_service import app as auth_app
# from MQ_service import app as mq_app
# from logging_functionality import create_log_file
import requests
# import multiprocessing
# import subprocess


# def start_service(script_name):
#     subprocess.run("venv/Scripts/activate.bat", shell=True)
#     subprocess.run(["python", script_name])

if __name__ == "__main__":
    # # Start auth service on port 8000
    # p1 = multiprocessing.Process(target=start_service, args=("auth_service.py",))
    # p1.start()

    # # Start MQ service on port 8001
    # p2 = multiprocessing.Process(target=start_service, args=("MQ_service.py",))
    # p2.start()
    
    
    # First step would be to log in as an admin
    token = requests.post(
        url="http://localhost:8000/auth/login/",
        json={"username": "admin", "password": "admin"},
    ).content
    # decode and get the token
    token = eval(token.decode("utf-8"))["token"]
    # Test get_queues()
    url = "http://localhost:7500/queue/"
    response = requests.get(url, params={"token": token})
    print("Getting all queues:")
    print(response.json())

    # Test get_queue()
    url = "http://localhost:7500/queue/{queue_id}"
    response = requests.get(url.format(queue_id='queue_job'), params={"token": token})
    print("Getting queue_job:")
    print(response.json())

    # Test get_queue_size()
    url = "http://localhost:7500/queue/{queue_id}/size"
    response = requests.get(url.format(queue_id="queue_job"), params={"token": token})
    print("Getting queue_job size:")
    print(response.text)

    # Test create_queue()
    url = "http://localhost:7500/queue/"
    response = requests.post(url, params={"token": token, "queue_id": 'new_queue'})
    print("Creating new_queue:")
    print(response.json())
    url = "http://localhost:7500/queue/"
    response = requests.get(url, params={"token": token})
    print("Getting all queues:")
    print(response.json())

    # Test delete_q()
    url = "http://localhost:7500/queue/{queue_id}/delete"
    response = requests.delete(url.format(queue_id='new_queue'), params={"token": token})
    print("Deleting new_queue:")
    print(response.json())
    url = "http://localhost:7500/queue/"
    response = requests.get(url, params={"token": token})
    print("Getting all queues:")
    print(response.json())

    # Test push()
    url = "http://localhost:7500/queue/{queue_id}/push"
    message = {"data": {"data": "test", "type": "test", "id": "test"}}
    response = requests.put(url.format(queue_id='queue_job'), params={"token": token}, json=message)
    print("Pushing to queue_job:")
    print(response.json())

    # Test pull()
    url = "http://localhost:7500/queue/{queue_id}/pull"
    response = requests.put(url.format(queue_id='queue_job'), params={"token": token})
    print("Pulling from queue_job:")
    print(response.json())
    
    
    # now i will try to push more messages than the max_queue_size
    print("Pushing more than the max_queue_size:")
    for i in range(6):
        url = "http://localhost:7500/queue/{queue_id}/push"
        response = requests.put(url.format(queue_id='queue_job'), params={"token": token}, json=message)
        print(response.json())
        # the last one should be an error
    
    # now i will try to pull from an empty queue
    url = "http://localhost:7500/queue/{queue_id}/pull"
    response = requests.put(url.format(queue_id='queue_result'), params={"token": token})
    print("Pulling from empty queue:")
    print(response.json())
    # now i will try to pull from an unexisting queue
    url = "http://localhost:7500/queue/{queue_id}/pull"
    response = requests.put(url.format(queue_id='queue_unexisting'), params={"token": token})
    print("Pulling from unexisting queue:")
    print(response.json())
    # now i will try to push to an unexisting queue
    url = "http://localhost:7500/queue/{queue_id}/push"
    response = requests.put(url.format(queue_id='queue_unexisting'), params={"token": token}, json=message)
    print("Pushing to unexisting queue:")
    print(response.json())
    # and now I will log in as secretary because he doesn't have any permissions
    token = requests.post(
        url="http://localhost:8000/auth/login/",
        json={"username": "secretary", "password": "secretary"},
    ).content
    token = eval(token.decode("utf-8"))["token"]
    url = "http://localhost:7500/queue/{queue_id}/push"
    response = requests.put(url.format(queue_id='queue_job'), params={"token": token}, json=message)
    print("Pushing to queue_job without permission:")
    print(response.json())
