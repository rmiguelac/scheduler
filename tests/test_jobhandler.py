from datetime import datetime
import re

import requests

JOBDETAILSHANDLER_URL = 'http://localhost:8888/job'
WRONG_JOB_ID = 'wrong'
GOOD_DATA = {"job_name": "busybox", "time": "5m"}
GOOD_ABSOLUTE_DATA = {"job_name": "busybox", "date": "27-06-2099 16:13:00"}
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
    assert f"{int((datetime.strptime(scheduled_to, '%d-%m-%Y %H:%M:%S') - datetime.strptime(scheduled_in, '%d-%m-%Y %H:%M:%S')).seconds / 60)}m" == GOOD_DATA['time']

def test_create_job_absolute_time_has_correct_date():
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_ABSOLUTE_DATA)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{id}")
    scheduled_to = response.json()['scheduled_to']
    assert scheduled_to == GOOD_ABSOLUTE_DATA['date']

def test_create_job_shows_status_scheduled_after_creation():
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_ABSOLUTE_DATA)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{id}")
    assert response.json()['status'] == "scheduled"

def test_delete_job_that_exists_returns_200():
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_ABSOLUTE_DATA)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    response = requests.delete(f"{JOBDETAILSHANDLER_URL}/{id}")
    assert response.status_code == 200

def test_delete_job_that_does_not_exists_returns_404():
    response = requests.delete(f"{JOBDETAILSHANDLER_URL}/wrong")
    assert response.status_code == 404

def test_delete_job_content_type_is_json():
    response = requests.delete(f"{JOBDETAILSHANDLER_URL}/wrong")
    assert 'application/json' in response.headers['Content-Type']

def test_deleted_job_is_moved_to_history():
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_ABSOLUTE_DATA)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    requests.delete(f"{JOBDETAILSHANDLER_URL}/{id}")
    response = requests.get(f"{JOBDETAILSHANDLER_URL}s")
    assert id in response.json()['history'].keys()

def test_deleted_job_status_is_canceled():
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_ABSOLUTE_DATA)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    requests.delete(f"{JOBDETAILSHANDLER_URL}/{id}")
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{id}")
    assert response.json()['status'] == 'canceled'

def test_deleted_job_finish_status_is_did_not_run():
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_ABSOLUTE_DATA)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    requests.delete(f"{JOBDETAILSHANDLER_URL}/{id}")
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{id}")
    assert response.json()['finish_status'] == 'did_not_run'

def test_finished_job_has_finish_date_key():
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_ABSOLUTE_DATA)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    requests.delete(f"{JOBDETAILSHANDLER_URL}/{id}")
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{id}")
    assert 'finish_date' in response.json().keys()

def test_finished_job_has_correct_format_finish_date():
    new_job = requests.post(f"{JOBDETAILSHANDLER_URL}", data=GOOD_ABSOLUTE_DATA)
    id = re.search('(?<=id ).*(?= will)', new_job.json()['message']).group()
    requests.delete(f"{JOBDETAILSHANDLER_URL}/{id}")
    response = requests.get(f"{JOBDETAILSHANDLER_URL}/{id}")
    try:
        fmt = bool(datetime.strptime(response.json()['finish_date'], '%d-%m-%Y %H:%M:%S'))
    except ValueError:
        fmt = False

    assert fmt == True
