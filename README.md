## EventBase Challenge 
I developed the challenge using the Flask framework and utilized the Celery Python package for executing asynchronous tasks. Celery can work with various message brokers, but for simplicity, I chose to use Redis for this project.  
For the preparation of each task, we could have had an additional queue and serialized it with the fetch service. However, due to time constraints, I didn't develop a second queue.  
I have made the decision to promptly rerun any failed jobs to minimize delays. However, to prevent an excessive accumulation of failing jobs and potential queue congestion, I have implemented a 'max attempt' field for each task. This field dictates the number of retries a task can undergo in case of continuous failures. If a task executes successfully, the attempt count is reset.  


### Database
This project consists of three tables: task, job, and data. The 'task' table is responsible for storing all information about a single task, including its start time, end time, and the interval for fetching new items.  
The 'job' table is responsible for storing the status of each task iteration's execution. This allows the user to retrieve the latest data or be informed about the status of the most recent task execution.  
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
It can be run within a while loop to ensure that all tasks are executed at precisely the required times.
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
### Api 
I have added an endpoint for adding new tasks and retrieving task results.
Swagger UI is available in below address 
```
http://localhost:8000/swagger-ui
```
In addition to Swagger UI, I have also added an Insomnia collection export in the project files, which can be used for testing APIs with Insomnia.  

##### Registering a user 
`POST /register`

##### Login a user and get token 
`POST /login`

##### Create a task 
`POST /tasks`

```
{
  "name": "task1",
  "url": "https://s3-us-west-2.amazonaws.com/eb-python-challenge/php-architecture/amazingexpo2020.json",
  "parameters": "{}",
  "start_time": "2023-01-04T21:41:38.930Z",
  "end_time": "2023-12-04T21:41:38.930Z",
  "task_interval": 100,
  "max_execution_time": 0,
  "max_attempt": 10
}
```
name: Task name.\
url: Task base url.\
parameters: Mixed parameters of a task for preparation before fetch.\
start_time: The start time of the year when the task is enabled.\
end_time: The end time of the year when the task is enabled.\
task_interval: The task execution frequency in seconds.\
max_execution_time: The Maximum time of execution of a task.\
max_attempt: The maximum number of attempts if a task continuously fails.

##### Get all tasks 
`GET /tasks`

It will return all tasks in the database, all information about tasks would be included. 
I'd like to mention that I also stored the last job status in the task entity. This decision was made to reduce complexity in handling a large number of tasks and to lessen the load on the database.

##### Get one task 
`GET /tasks/{task_id}`

##### Delete a task 
`DELETE /tasks/{task_id}`

##### Get status of af one task 
`GET /tasks/{task_id}/status`

###### Response
```angular2html
{
	"execution_time": 0,
	"id": 2,
	"last_execute_time": "2023-10-05T03:41:39",
	"last_execution_data": null,
	"last_execution_error": "Expecting value: line 1 column 1 (char 0)",
	"last_execution_status": "TaskStatus.Failed"
}
```
- execution_time: How long did task take to execute last time.  
- id: task id.  
- last_execute_time: The last time task executed.  
- last_execution_data: The response of the URL in the last execution: If the task finished without error, it will reload all fetched data.
- last_execution_error: The last execution error description 
- last_execution_status: Tha last execution status 

##### Reset maximum attempts of a task
If a task continuously fails and its maximum attempts exceed the threshold, this API allows us to reset it.  
`POST /tasks/{task_id}/reset-attempt`


### Feature works
If I had more time, I would like to add below list to the application 
1. Increase the level of logging to capture the status of each job execution. 
2. Implement more comprehensive exception handling for various situations.
3. I would like to learn more about access levels and how to develop access levels for executing each job.
4. Configure the database for Celery to capture task execution information more precisely.
