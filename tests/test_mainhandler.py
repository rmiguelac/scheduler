import requests

MAINHANDLER_URL = 'http://localhost:8888'

def test_get_mainhandler_status_code_200():
    response = requests.get(MAINHANDLER_URL)
    assert response.status_code == 200

def test_get_mainhandler_content_type_is_json():
    response = requests.get(MAINHANDLER_URL)
    
    # Here we use in and not  == because we can have the charset
    assert "application/json" in response.headers["Content-Type"] 

def test_get_mainhandler_redirect_to_jobs():
    response = requests.get(MAINHANDLER_URL)
    assert response.url == f"{MAINHANDLER_URL}/jobs"
