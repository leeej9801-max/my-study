from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

arr = []

@app.get("/")
def root(txt: str = ""):
  return {"status": True, "txt": txt}

@app.post("/{var}")
def root(
  var: str = "",
  id: str = Form(""), 
  pwd: str = Form("")
):
  return {"status": True, "id": id, "pwd": pwd, "var": var}

@app.get("/view", response_class=HTMLResponse)
def view():
  return """
    <body>
      <form action="/2" method="post">
        <input type="text" name="id" />
        <input type="password" name="pwd" />
        <button type="submit">요청</button>
      </form>
    </body>
  """
