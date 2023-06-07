# API Assignement

## Run
* python3 auth_service.py
* python3 master_data_service.py
* to get the token you can log in with the following credentials:
    * username: admin
    * password: admin
* afterwards you can use the token to access all the other services

## Services
### auth_service.py (/auth) PORT: 8000
* GET
    * /users - gets all the users, just for testing
* POST
    * /login - takes a username and password and returns a token
        * username: admin
        * password: admin
    * /manage - takes a token and body(username, password, role) and creates a new user. the creator of the user has to be an admin
* DELETE
    * /manage - takes a token and body(username) and deletes the user. the requester has to be an admin
* PUT
    * /manage - takes a token and body(username, role) and updates the user. the requester has to be an admin
### master_data_service.py (/master) PORT: 8001
* GET
    * /jobs - takes a token and returns all the jobs
    * /results - takes a token and returns all the results
* POST
    * /jobs - takes a token and body(daterange and assets) and creates a new job
    * /results - takes a token and body(job_id and assers) and creates a new result
* PUT
    * /jobs - takes a token and body(job_id) and changes the status of the job to in progress

## Other files
### auth.py
* contains the authentication logic
* generates a token that contains the username and is valid for 15 minutes
* checks if the token is valid
* stores the users in a dictionary
* encodes and decodes the token
* hashes the password
### schemas.py
* contains the schemas for the requests and responses
* contains all the classes

## Database 
* the database is represented by 2 json files
    * jobs.json - contains all the jobs with the following structure
        ```json
        {
            "job_id": "string",
            "user": "string",
            "timestamp": "string",
            "status": "string",
            "date_range": "string",
            "assets": "list[int]"
        }
        ```
    * results.json
        ```json
        {
            "job_id": "string",
            "timestamp": "string",
            "assets": "list[float]"
        }
        ```
## Design Decisions
* <b>REST</b> is a popular choice for web-based applications because it is simple, lightweight, highly scalable, flexible, supports caching, and widely adopted.
* <b>FastAPI</b> is a popular choice for building APIs with Python because it is fast, easy to use, and provides several advanced features, such as automatic documentation generation, type hints, async support, and data validation.
* <b>JWT</b> is a popular choice for authentication because it is stateless, secure, and widely supported by many programming languages and platforms.
* <b>JSON</b> is a lightweight, easy-to-read, write and code with.