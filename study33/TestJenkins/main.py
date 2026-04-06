from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ReqModel(BaseModel):
  a: int
  b: int

@app.get("/")
def read_root():
  return {"status": False}

@app.post("/")
def read_root(model: ReqModel):
  return {"result": model.a + model.b}

@app.put("/")
def save_root(model: ReqModel):
  return {"v1": model.a, "v2": model.b}

