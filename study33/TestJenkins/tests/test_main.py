from fastapi.testclient import TestClient
from App.main import app

client = TestClient(app)

def test_get_read_root():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"status": False}

def test_post_read_root():
  payload = {"a": 4, "b": 5}
  response = client.post("/", json=payload)
  assert response.status_code == 200
  assert response.json() == {"result": 9}

def test_put_save_root():
  payload = {"a": 4, "b": 5}
  response = client.put("/", json=payload)
  assert response.status_code == 200
  assert response.json() == {"v1": 4, "v2": 5}
