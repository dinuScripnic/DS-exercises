# MPI Service
Scripnic Dinu and David Bobek engineering

## Run
* python3 auth_service.py
* python3 MQ_service.py
* python3 MPI_service.py
* most porbably you will need to generate some jobs using job_generator.py
* I will try to create a dockerfile and docker-compose file to make it easier to run the project

## MPI Service
1. MPI service will log in to get the token
2. Start the loop for processing the jobs
3. IF the rank is 0, pull a job from the queue 
    * If no jobs are available, wait for 3 seconds and try again
4. Extract job details
5. Scatter tassk accross processes based on assets
6. Perform the tasks
7. Gather the results
8. Push the results to the results queue