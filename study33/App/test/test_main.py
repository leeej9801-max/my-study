# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from App.main import app

client = TestClient(app)

def test_get_read_root():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"status": True}

def test_post_read_root():
  payload = {"a": 3, "b": 5}
  response = client.post("/", json=payload)
  assert response.status_code == 200
  assert response.json() == {"result": 8}
