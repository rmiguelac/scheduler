import re

import requests
import pytest

JOBDETAILSHANDLER_URL = 'http://localhost:8888/job'
WRONG_JOB_ID = 'wrong'

def test_get_job_details_non_existing_job_returns_404():
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{WRONG_JOB_ID}")
    assert response.status_code == 404

def test_get_job_details_from_non_existing_job_returns_expected_message():
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{WRONG_JOB_ID}")
    assert response.json() == {"message": f"job with id {WRONG_JOB_ID} not found"}

def test_get_job_details_content_type_is_json():
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{WRONG_JOB_ID}")
    assert "application/json" in response.headers["Content-Type"]

def test_get_job_details_existing_job_returns_200():
    data = {
        "job_name": "SAMPLE_200_JOB",
        "time": "200m"
    }
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=data)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{id}")
    assert response.status_code == 200

def test_get_job_details_existing_job_has_expected_keys():
    data = {
        "job_name": "SAMPLE_KEYS_JOB",
        "time": "100m"
    }
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=data)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{id}")
    ekeys = ["id", "job_name", "scheduled_in", "scheduled_to", "status"]
    for ekey in ekeys:
        if not ekey in response.json().keys():
            pytest.fail(f"Missing key {ekey} from {ekeys} in {response.json().keys()}")