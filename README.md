# **Scheduler**

Scheduler is an API developed with python's web framework [tornado](https://www.tornadoweb.org/en/stable/) which makes easy to handle async and non-blocking network I/O.  
Since scheduler should be a production-grade code, no blocking calls should happen, allowing for multiple jobs to run/be scheduled at the same time.  

## **Design Decisions**

First and foremost, the choice for python language was purely based upon the familiarity with its syntax and general built-in packages and frameworks. We could have used golang which was designed to handle high volumes of requests, making use of multi-thread, coroutines and the-like, yet it would not be delivered in time.  
Tornado choice was purely based on it's ability to provide async functionalities.  
To avoid having an empty endpoint for '/', it redirects to '/jobs'.  
The decision to enable jobs to be scheduled by either providing relative or absolute time was for end-user convinience.  
Since we have jobs that can be in the running state or in scheduled state, as well as jobs that are in the history (ran or were canceled), the ```DELETE``` method would only make sense in this context if we were to delete it from the scheduled list, effectively de-scheduling it. Remove if from the running list would mean we would like to kill it, which as of now is not part of the requirements. Also, remove something from the history would only obscure system state since we would have no records of it.

## **Installing**


## **Using**
Once the application is up and running, the following endpoints are exposed:

- **GET /**    
    summary: redirects to /jobs  
    example call: ```curl --location --request GET 'localhost:8888/jobs'```  
    example response:  
    ```json
    {
        "running": {},
        "scheduled": {
            "71f6696c08a64a45b3788332e0dc5278": {
                "id": "71f6696c08a64a45b3788332e0dc5278",
                "job_name": "JOB_A",
                "scheduled_in": "20-06-2021 13:24:58",
                "scheduled_to": "20-06-2021 13:25:28",
                "status": "scheduled"
            }
        },
        "history": {}
    }
    ```
- **GET /jobs**    
    summary: list all jobs, them being in ```running```, ```scheduled``` state or in the ```history``` if it finishes or is deleted from the schedule.  
    example call: ```curl --location --request GET 'localhost:8888/job/38c24e78de0646b2a7348cfa6fc2035c'```  
    example response:  
    ```json
    {
        "running": {},
        "scheduled": {
            "71f6696c08a64a45b3788332e0dc5278": {
                "id": "71f6696c08a64a45b3788332e0dc5278",
                "job_name": "JOB_A",
                "scheduled_in": "20-06-2021 13:24:58",
                "scheduled_to": "20-06-2021 13:25:28",
                "status": "scheduled"
            }
        },
        "history": {}
    }
    ```

- **POST /job**  
    summary: show details of a single job  
    parameters:  
        - ```job_name```: job/image to run  
        - ```date```: relative or absolute date to schedule job to run  
    returns: ```application/json```  
    example call: ```curl --location --request POST 'localhost:8888/job' --form 'job_name="JOB_A"' --form 'date="30s"'```  
    example response:  
    ```json
    {
        "message": "job JOB_A with id 71f6696c08a64a45b3788332e0dc5278 will be scheduled to run in 30s"
    }
    ```

- **DELETE /job**
    summary: delete a scheduled job (de-schedule it)  
    parameters:  
        - ```job_id```    
    returns: ```application/json```  
    example call: ```curl --location --request DELETE 'localhost:8888/job/15a3e3387c2f44eb89cc62099046353a'```  
    example response:  

## **Testing**


    
## **Tech-stack**

- [Tornado](https://www.tornadoweb.org/en/stable/)
- [Python 3.8](https://www.python.org/downloads/release/python-382/)