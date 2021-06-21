import requests

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
    pass

def test_get_job_details_existing_job_has_expected_keys():
    pass

