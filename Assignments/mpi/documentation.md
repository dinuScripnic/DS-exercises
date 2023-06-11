# MQ service
Scripnic Dinu and David Bobek engineering


## Run
* python3 auth_service.py
* python3 MQ_service.py
* to get the token you can log in with the following credentials:
    * username: admin
    * password: admin
* afterwards you can use the token to access all the other services
* to access auth service you can go to http://localhost:8000/docs . There are all the API calls
* to access MQ service you can go to http://localhost:7500/docs . There are all the API calls
* Also we provided a test script for the MQ service. You can run it with the following command:
    * python3 proof.py

## Authentication
* For authentificationwe are using the same auth server as for assignment 2.
* Only difference between is that now we added the logging functionality.
* This service will run on port 8000

## Config file
* The config file is called config.yml and is located in the root directory of the project.
* It contains:
    * the port on which the service will run
    * max queue size
    * persist interval
    * path to queue database
    * roles and their permissions
    * logging data

## Message Queue
* GET
    * /queue - takes a token and returns all the queues
    * /queue/{queue_id} - takes a token and returns the queue with the given id
    * /queue/{queue_id}/size - takes a token and returns the size of the queue with the given id
* POST
    * /queue - takes a token and body(queue_id) and creates a new queue with the given id
* DELETE
    * /queue/{queue_id} - takes a token and deletes the queue with the given id, also all the messages in that queue are deleted
* PUT   
    * /queue/{queue_id}/pull - takes a token and body(message) and adds the message to the queue with the given id
    * /queue/{queue_id}/pull - takes a token and returns the first message from the queue with the given id, also deletes that message from the queue

## Logging
* The logging is done with the help of the python logging module.
* The logs are stored in message_queue.log file.
* logs have the following format:
    * timestamp
    * level
    * message (code + description)

## Queue Saving
* The queues are saved as json files in the queues.json file.
* The queues are saved every 30 seconds. Can be changed in the config file.