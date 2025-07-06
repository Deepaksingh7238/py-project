import requests
import json
BASE_URL = "http://localhost:8000/api"
def test_job_portal():
    company_data = {
        "name": "Test Company",
        "location": "Test Location",
        "description": "Test Description"
    }
    response = requests.post(f"{BASE_URL}/create-company/", json=company_data)
    print(f"Create Company: {response.status_code} - {response.json()}")
    job_data = {
        "company_id": 1,
        "title": "Test Job",
        "description": "Test Job Description",
        "salary": 50000,
        "location": "Remote"
    }
    response = requests.post(f"{BASE_URL}/post-job/", json=job_data)
    print(f"Post Job: {response.status_code} - {response.json()}")
    response = requests.get(f"{BASE_URL}/jobs/")
    print(f"Get Jobs: {response.status_code} - {response.json()}")
def test_blog_system():
    session = requests.Session()
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    response = session.post(f"{BASE_URL}/register/", json=user_data)
    print(f"Register: {response.status_code} - {response.json()}")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = session.post(f"{BASE_URL}/login/", json=login_data)
    print(f"Login: {response.status_code} - {response.json()}")
    post_data = {
        "title": "Test Post",
        "content": "This is a test post content"
    }
    response = session.post(f"{BASE_URL}/create-post/", json=post_data)
    print(f"Create Post: {response.status_code} - {response.json()}")
    response = session.get(f"{BASE_URL}/posts/")
    print(f"Get Posts: {response.status_code} - {response.json()}")
if __name__ == "__main__":
    print("Testing Job Portal API...")
    test_job_portal()
    print("\nTesting Blog System API...")
    test_blog_system()
