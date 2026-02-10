import { Routes, Route } from "react-router";

const NotFound = () => {
  return (
    <div className="container mt-3 text-center">
      <h1>404</h1>
      <p>페이지를 찾을 수 없습니다.</p>
    </div>
  )
}

const Home = () => {
  return (
    <div className="container mt-3 text-center">
      <h1>메인 화면</h1>
    </div>
  )
}

function App() {
  const paths = [
    {path: "/", element: <Home />},
    {path: "*", element: <NotFound />},
  ]
  return (
    <>
      <Routes>
        { paths?.map((v, i) => <Route key={i} path={v.path} element={v.element} />) }
      </Routes>
    </>
  )
}

export default App
