import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from fastapi.testclient import TestClient
from main import app

def test_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "MCP Server is running."

def test_agent_message():
    client = TestClient(app)
    payload = {"text": "hello"}
    response = client.post("/agent/message", json=payload)
    assert response.status_code == 200
    assert response.json()["received"] == payload
