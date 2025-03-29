from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

def test_read_index():
    response = client.get("/")
    assert response.status_code == 200

def test_generate_text():
    response = client.post(
        "/api/generate",
        json={"prompt": "Hello, world!", "max_length": 50, "temperature": 0.8},
    )
    assert response.status_code == 200
    assert "generated_text" in response.json()
    assert "Hello, world!" in response.json()["generated_text"]