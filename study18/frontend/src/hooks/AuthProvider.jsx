import { createContext, useContext, useState, useEffect } from "react"
import { useNavigate } from "react-router";
import axios from "axios"

const api = axios.create({
  baseURL: import.meta.env.VITE_APP_FASTAPI_URL || "http://localhost:8000",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
})

export const AuthContext = createContext()

const AuthProvider = ({children}) => {
  const [isLogin, setIsLogin] = useState(false)
  const navigate = useNavigate()

  const setAuth = status => {
    localStorage.setItem("user", status)
    setIsLogin(status)
    navigate("/")
  }

  const removeAuth = () => {
    
    api.post("/logout")
    .then(res => {
      console.log(res)
      localStorage.removeItem("user")
      setIsLogin(false)
      navigate("/")
    })
    .catch(err => console.error(err))
    
  }

  useEffect(() => {
    if(localStorage.getItem("user")) setIsLogin(true)
  }, [])

  return (
    <AuthContext.Provider value={{ isLogin, setAuth, removeAuth }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)

export default AuthProvider