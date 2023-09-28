## EventBase Challenge 
I developed the challenge using the Flask framework and utilized the Celery Python package for executing asynchronous tasks. Celery can work with various message brokers, but for simplicity, I chose to use Redis for this project.\
For the preparation of each task, we could have had an additional queue and serialized it with the fetch service. However, due to time constraints, I didn't develop a second queue.
### Database
This project consists of three tables: task, job, and data. The 'task' table is responsible for storing all information about a single task, including its start time, end time, and the interval for fetching new items.\
The 'job' table is responsible for storing the status of each task iteration's execution. This allows the user to retrieve the latest data or be informed about the status of the most recent task execution.\
The 'data' table is used for storing parsed received data. It is related to each job, enabling us to associate responses with specific jobs.

### Installation

For starting project please execute following command in root folder
```angular2html
docker-compose up --build 
```

For database initialization execute following commads
```angular2html
docker exec website challenge db init 
```

For testing purposes, I have created a CLI command to seed the database. It will add 10 tasks to the database.
```angular2html
docker exec website challenge db seed 
```
To initiate the task of fetching all tasks, I have developed a CLI command. However, it can be moved to a Docker Compose command and run in a while loop to ensure that all tasks will execute at their required times. For scheduling the task for the fetch service, you can use the following command:
```angular2html
docker exec website challenge feed
```

In order to run all tests, following command can be used
```angular2html
docker exec website challenge test
```

Also for test code coverage, following command can be used
In order to run all tests, following command can be used
```angular2html
docker exec website challenge cov
```

### Feature works
If I had more time, I would like to add below list to the application 
1. Increase the level of logging to capture the status of each job execution. 
2. Implement more comprehensive exception handling for various situations.
3. I would like to learn more about access levels and how to develop access levels for executing each job.
4. Configure the database for Celery to capture task execution information more precisely.
