import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { BrowserRouter, Routes, Route } from "react-router";
import "@/style.css"

const Nav = () => {
  return (
    <nav className="navbar navbar-expand-sm bg-dark navbar-dark">
      <div className="container-fluid">
        <a className="navbar-brand" href="/">HOME</a>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="collapsibleNavbar">
          <ul className="navbar-nav">
            <li className="nav-item">
              <a className="nav-link" href="/signIn">SignIn</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/signUp">SignUp</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/user">User</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/404">404</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/html/main.html" target="_blank">예시화면1</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/html/signIn.html" target="_blank">예시화면2</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/html/signUp.html" target="_blank">예시화면3</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/html/user.html" target="_blank">예시화면4</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  )
}
const Footer = () => {
  const styles = {color: "#7eb047", fontWeight: "bold"}
  return (
    <div className="mt-5 p-4 bg-dark text-white text-center">
      <p>SHELL<span style={styles}>FOLDER</span></p>
    </div>
  )
}
const Main = () => {
  return (
    <h1 className="text-center">기본 화면</h1>
  )
}
const SignIn = () => {
  return (
    <h1 className="text-center">로그인 화면</h1>
  )
}
const SignUp = () => {
  return (
    <h1 className="text-center">회원가입 화면</h1>
  )
}
const User = () => {
  return (
    <h1 className="text-center">사용자 정보 화면</h1>
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
    {path: "/", element: <Main />},
    {path: "/signIn", element: <SignIn />},
    {path: "/signUp", element: <SignUp />},
    {path: "/user", element: <User />},
    {path: "*", element: <NotFound />},
  ]
  return (
    <>
      <Nav />
      <div className="container-fluid mt-3" style={{minHeight: '50vh'}}>
        <BrowserRouter>
          <Routes>
            {
              paths?.map((v, i) => <Route key={i} path={v.path} element={v.element} />)
            }
          </Routes>
        </BrowserRouter>
      </div>
      <Footer />
    </>
  )
}
export default App
