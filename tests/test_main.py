import sys
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from main import app

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

load_dotenv()

client = TestClient(app)
base = os.getenv("BASE_URL")

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Intro":"Welcome to CSEDUIC backend"}

def test_sign_up_and_signin():
    response =client.post(f"{base}/auth/signup",json={
        "user_name":"testuser",
        "email":"test@gmail.com",
        "password":"0Testpassword!"
    })

    assert response.status_code == 201
    assert response.json() == {"message":"User created successfully"}

    response = client.post(f"{base}/auth/signin",json={
        "email":"test@gmail.com",
        "password":"0Testpassword!"
    })

    assert response.status_code == 200

    user_id = response.json()["user_id"]

    response = client.delete(f"{base}/auth/{user_id}")




