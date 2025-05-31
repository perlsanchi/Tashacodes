from app import app

def test_home_page():
    # Creates a test client using the Flask application
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data or b"Sign Up" in response.data
