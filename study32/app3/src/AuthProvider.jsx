import { createContext, useContext, useState, useEffect } from "react"
import { useNavigate } from "react-router";

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
const Page1 = () => {
  return (
    <div className="container mt-3 text-center">
      <h1>페이지1 화면</h1>
    </div>
  )
}
const Page2 = () => {
  return (
    <div className="container mt-3 text-center">
      <h1>페이지2 화면</h1>
    </div>
  )
}

const getPath1 = () => {
  return [
    {path: "/", element: <Home />},
    {path: "*", element: <NotFound />},
  ]
}

const getPath2 = () => {
  return [
    {path: "/", element: <Home />},
    {path: "/page1", element: <Page1 />},
    {path: "/page2", element: <Page2 />},
    {path: "*", element: <NotFound />},
  ]
}

export const AuthContext = createContext()

const AuthProvider = ({children}) => {
  const [isPending, setIsPending] = useState(false)
  const [isLogin, setIsLogin] = useState(false)
  const navigate = useNavigate()

  const setAuth = status => {
    localStorage.setItem("user", status);
    setIsLogin(status);
    navigate("/");
  }

  const clearAuth = () => {
    localStorage.removeItem("user")
    setIsLogin(false)
    navigate("/")
  }

  const [paths, setPaths] = useState(getPath1())
  useEffect(()=>{
    if(localStorage.getItem("user")) {
      setIsLogin(true)
      setPaths(getPath2())
    } else {
      setPaths(getPath1())
    }
    setIsPending(true)
  }, [isLogin])

  return (
    <AuthContext.Provider value={{ paths, setAuth, clearAuth, isLogin, isPending }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)

export default AuthProvider