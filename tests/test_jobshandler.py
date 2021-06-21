import requests

JOBSHANDLER_URL = "http://localhost:8888/jobs"

def test_jobs_handler_status_code_is_200():
    response = requests.get(JOBSHANDLER_URL)
    assert response.status_code == 200

def test_jobs_content_type_is_json():
    response = requests.get(JOBSHANDLER_URL)
    assert "application/json" in response.headers["Content-Type"]

def test_jobs_output_has_keys_running_scheduled_history():
    response = requests.get(JOBSHANDLER_URL)
    assert response.json() == {'running': {}, 'scheduled': {}, 'history': {}}
