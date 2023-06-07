from schemas import Queue
import json
import yaml
import time
import threading


with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

queue_file_path = config["queues_file"]["file_path"]
max_queue_size = config["queues_file"]["max_queue_size"]
queue_save_interval = config["queues_file"]["persist_interval"]

def initialize_queues() -> list[Queue]:
    """
    If the queues file exists, it loads the queues from the file.
    If the queues file doesn't exist, it creates a new file and initializes the queues with two empty queues.
    """
    try:
        with open(queue_file_path, "r") as f:
            queues = json.load(f)  # list[Queue]
            queues = [Queue(**queue) for queue in queues]
            
        
    except FileNotFoundError:
        # Initialize the queues with two empty queues
        queues = [
            Queue(
                max_size=max_queue_size,
                queue_id="queue_job",
                queues=[],
            ),
            Queue(
                max_size=max_queue_size,
                queue_id="queue_result",
                queues=[],
            )
        ]
        
    return queues

queues = initialize_queues()


def check_exist(queue_id:str) -> bool:
    """
    Searches for a queue with the specified id.
    Returns True if the queue exists, False otherwise.

    Args:
        queue_id (str): queue id

    Returns:
        bool: True if the queue exists, False otherwise
    """
    for queue in queues:
        if queue.queue_id == queue_id:
            return True
    return False


def search_queue(queue_id:str) -> Queue|None:
    """
    Returns the queue with the specified id.

    Args:
        queue_id (str): queue id

    Returns:
        dict: queue data
    """
    for queue in queues:
        if queue.queue_id == queue_id:
            return queue
    return None


def delete_queue(queue_id:str) -> None:
    """
    Deletes the queue with the specified id.

    Args:
        queue_id (str): queue id
    """
    for queue in queues:
        if queue.queue_id == queue_id:
            queues.remove(queue)
            break


class QueueSaver:
    def __init__(self):
        """
        Initializes the QueueSaver class.
        """
        self.queues = queues
        self.filename = queue_file_path
        self.save_interval = queue_save_interval
        self.save_thread = threading.Thread(target=self.save_queues_periodically, daemon=True)
    
    def start(self):
        """
        Starts the thread that saves the queues periodically.
        """
        self.save_thread.start()
    
    def save_queues_periodically(self):
        """
        Saves the queues periodically. The interval is specified in the config file.
        """
        while True:
            self.save_queues()
            time.sleep(self.save_interval)
    
    def save_queues(self):
        """
        Saves the queues to the file.
        """
        with open(self.filename, 'w') as f:
            q = [queue.__dict__ for queue in self.queues]
            json.dump(q, f)


if __name__ == "__main__":
    # for testing purposes, LGTM
    print(search_queue("queue_job"))
    print(search_queue("queue_result1"))
    print(check_exist("queue_job"))
    print(check_exist("queue_results"))