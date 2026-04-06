import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { BrowserRouter, Routes, Route } from "react-router";
import axios from 'axios'
import { useState } from 'react'
import { jwtDecode } from "jwt-decode"

const api = axios.create({
  baseURL: import.meta.env.VITE_APP_FASTAPI_URL || "http://localhost:8000",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
})

const Login = () => {
  const [email, setEmail] = useState("")
  const [pwd, setPwd] = useState("")

  const submitEvent = e => {
    e.preventDefault()
    const params = { email, pwd }
    api.post("/login", params)
    .then(res => {
      console.log(res)
    })
  }
  const meEvent = () => {
    api.get("/me")
    .then(res => {
      console.log(res)
      if(res.data.status) alert(res.data.me)
    })
  }

  return (
    <div className="container mt-3">
			<h1 className="display-1 text-center">로그인</h1>
			<form onSubmit={submitEvent}>
				<div className="mb-3 mt-3">
					<label htmlFor="email" className="form-label">이메일</label>
					<input type="email" className="form-control" id="email" placeholder="이메일를 입력하세요." value={email} onChange={e=>setEmail(e.target.value)} />
				</div>
				<div className="mb-3">
					<label htmlFor="pwd" className="form-label">비밀번호</label>
					<input type="password" className="form-control" id="pwd" placeholder="비밀번호를 입력하세요." value={pwd} onChange={e=>setPwd(e.target.value)} />
				</div>
        <div className="d-flex">
          <div className="p-2 flex-fill d-grid">
            <button type="submit" className="btn btn-primary">로그인</button>
          </div>
          <div className="p-2 flex-fill d-grid">
            <button type="button" className="btn btn-primary" onClick={meEvent}>취소</button>
          </div>
        </div>
			</form>
		</div>
  )
}

const Home = () => {
  const callEvent = () => {
    console.log("callEvent")
    axios.get("http://localhost:8000/")
    .then(res => {
      console.log(res)
      if(res.data.status) alert(res.data.msg)
    })
  }
  return (
    <div className="text-center">
      <h1>메인 화면입니다.</h1>
      <button type="button" onClick={callEvent}>FastAPI 호출</button>
      <a href="/login">로그인</a>
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
    {path: "/login", element: <Login />},
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