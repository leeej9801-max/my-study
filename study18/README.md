## FrontEnd `React`
- 프로젝트 생성 (vite)

```bash
npm create vite .
```

- React-Router 설치

```bash
npm i react-router
```

- 비동기통신 `axios` 설치

```bash
npm i axios
```

- 스타일 프레임워크 `Bootstrap` 설치

```bash
npm i bootstrap bootstrap-icons
```

- React 기본 설정 `app.jsx`

```js
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { BrowserRouter, Routes, Route } from "react-router";

const Home = () => {
  return (
    <div className="text-center">
      <h1>메인 화면입니다.</h1>
    </div>
  )
}

const NotFound = () => {
  return (
    <div className="text-center">
      <h1>404</h1>
      <p>페이지를 찾을 수 없습니다.</p>
    </div>
  )
}

const App = () => {
  const paths = [
    {path: "/", element: <Home />},
    {path: "*", element: <NotFound />},
  ]
  return (
    <>
      <BrowserRouter>
        <Routes>
          { paths?.map((v, i) => <Route key={i} path={v.path} element={v.element} />) }
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
```

- React 실행 `Service Run` 개발모드

```bash
npm run dev
```

## BackEnd `FastAPI`
- 프로젝트 생성 (uv)

```bash
uv init .
```

- FastAPI 설치

```bash
uv add fastapi --extra standard
```

- FastAPI 기본 설정 `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}
```

- FastAPI 실행 `Service Run` 개발모드

```bash
uv run fastapi dev
```
