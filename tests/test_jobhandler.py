from datetime import datetime, timedelta
import re

import requests

from config import DATE_FORMAT

JOBDETAILSHANDLER_URL = 'http://localhost:8888/job'
WRONG_JOB_ID = 'wrong'
GOOD_DATA = {"job_name": "busybox", "time": "5m"}
BAD_DATA = {"jobname": "busybox", "time": "10m"}


def test_create_job_returns_200():
    response = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_DATA)
    assert response.status_code == 200

def test_create_job_with_wrong_input_returns_400():
    data = {
        "jobname": "busybox",
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
    scheduled_in = response.json()['scheduled_in']
    scheduled_to = response.json()['scheduled_to']
    assert f"{int((datetime.strptime(scheduled_to, DATE_FORMAT) - datetime.strptime(scheduled_in, DATE_FORMAT)) / 60)}m" == GOOD_DATA['time']

def test_create_job_absolute_time_has_correct_date():
    pass

def test_create_job_shows_status_scheduled_after_creation():
    pass
