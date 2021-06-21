# **Scheduler**

**Scheduler** is a simple async API to schedule docker-based jobs.

Scheduler allows the end-user to schedule jobs by its name at a relative or absolute time

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
    **summary:** redirects to /jobs  
    **returns:** ```application/json```
    **example call:** ```curl --location --request GET 'localhost:8888/jobs'```  
    **example response:**  
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
    **summary:** list all jobs, them being in ```running```, ```scheduled``` state or in the ```history``` if it finishes or is deleted from the schedule.  
    **returns:** ```application/json```  
    **example call:** ```curl --location --request GET 'localhost:8888/job/38c24e78de0646b2a7348cfa6fc2035c'```  
    **example response:**  
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

- **GET /job**  
    **summary:** get job details
    **returns:** ```application/json```  
    **parameters:**  
        - ```job_id```: job id
    **example call:** ```curl --location --request GET 'localhost:8888/job/8b2a719840f643cf9f657d1c1af78955'```  
    **example response:**    
    ```json
    {
        "id": "8b2a719840f643cf9f657d1c1af78955",
        "job_name": "JOB_ABSOLUTE",
        "scheduled_in": "20-06-2021 16:12:19",
        "scheduled_to": "20-06-2021 16:13:00",
        "status": "scheduled"
    }
    ```

- **POST /job**  
    **summary:** schedule a single job to run at a given time.  
    **long description:** Given a job, schedule it at a given time where the date can be given in two forms: relative (30s, 2m, 1h, 4d, always round and not 2h30m) or absolute in the "%d-%m-%Y %H:%M:%S" date format, for example "20-06-2021 20:00:00"  
    **returns:** ```application/json```  
    **parameters:**  
        - ```job_name```: job/image to run  
        - ```date```: absolute date to schedule job to run  _OR_ ```time```: for relative time schedule.  
    **example call (relative date):** ```curl --location --request POST 'localhost:8888/job' --form 'job_name="JOB_B"' --form 'time="2m"'```  
    **example response (relative date):**    
    ```json
    {
        "message": "job JOB_B with id affae502278b44cf95ea4bd7ad9e6265 will be scheduled to run in 2m"
    }
    ```
        
    **example call (absolute date):** ```curl --location --request POST 'localhost:8888/job' --form 'job_name="JOB_ABSOLUTE"' --form 'date="20-06-2021 16:13:00"'```  
    **example response (absolute date):**  
    ```json
    {
        "message": "job JOB_ABSOLUTE with id 8b2a719840f643cf9f657d1c1af78955 will be scheduled to run in 20-06-2021 16:13:00"
    }
    ```

- **DELETE /job**
    **summary:** delete a scheduled job (de-schedule it)  
    **parameters:**  
        - ```job_id```: job id  
    **returns:** ```application/json```  
    **example call:** ```curl --location --request DELETE 'localhost:8888/job/6bfde86edc8c4edf91eec8ef70c90a45'```  
    **example response:**  
    ```json
    {
        "message": "job 6bfde86edc8c4edf91eec8ef70c90a45 was de-scheduled"
    }
    ```

## **Testing**


    
## **Tech-stack**

- [Tornado](https://www.tornadoweb.org/en/stable/)
- [Python 3.8](https://www.python.org/downloads/release/python-382/)