from datetime import datetime, timedelta
import re

import requests

JOBDETAILSHANDLER_URL = 'http://localhost:8888/job'
WRONG_JOB_ID = 'wrong'
GOOD_DATA = {"job_name": "GOOD_JOB", "time": "5m"}
BAD_DATA = {"jobname": "BAD_JOB", "time": "000m"}


def test_create_job_returns_200():
    response = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_DATA)
    assert response.status_code == 200

def test_create_job_with_wrong_input_returns_400():
    data = {
        "jobname": "CREATE_JOB_400",
        "tim": "200m"
    }
    response = requests.post(f"{JOBDETAILSHANDLER_URL}", data=BAD_DATA)
    assert response.status_code == 400

def test_create_job_content_type_is_json():
    response = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_DATA)
    assert "application/json" in response.headers["Content-Type"]

def test_create_job_relative_time_sums_date_correctly():
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_DATA)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{id}")
    scheduled_on = response.json()['scheduled_on']
    scheduled_to = response.json()['scheduled_to']

def test_create_job_absolute_time_has_correct_date():
    pass

def test_create_job_shows_status_scheduled_after_creation():
    pass
