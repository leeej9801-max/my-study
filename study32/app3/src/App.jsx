import { Routes, Route } from "react-router";
import { useAuth } from '@/AuthProvider.jsx'

function App() {
  const { paths, setAuth, clearAuth, isLogin, isPending } = useAuth()
  return (
    <>
      {
        isPending &&
        <div>
          {!isLogin && <button type="button" onClick={()=>setAuth(true)}>로그인</button>}
          {isLogin && <button type="button" onClick={()=>clearAuth()}>로그아웃</button>}
        </div>
      }
      <Routes>
        { paths?.map((v, i) => <Route key={i} path={v.path} element={v.element} />) }
      </Routes>
    </>
  )
}

export default App
