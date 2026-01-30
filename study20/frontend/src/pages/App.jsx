import { Routes, Route } from "react-router";
import '@styles/App.css'
import NotFound from '@pages/NotFound.jsx'
import Nav from '@pages/Nav.jsx'
import Home from '@pages/Home.jsx'
import Login from '@pages/Login.jsx'
import SignUp from '@pages/SignUp.jsx'
import UserView from '@pages/UserView.jsx'
import UserEdit from '@pages/UserEdit.jsx'
import BoardAdd from '@pages/BoardAdd.jsx'
import BoardView from '@pages/BoardView.jsx'
import BoardEdit from '@pages/BoardEdit.jsx'

function App() {
   const paths = [
    {path: "/", element: <Home />},
    {path: "/login", element: <Login />},
    {path: "/signup", element: <SignUp />},
    {path: "/userview", element: <UserView />},
    {path: "/useredit", element: <UserEdit />},
    {path: "/boardadd", element: <BoardAdd />},
    {path: "/boardview/:no", element: <BoardView />},
    {path: "/boardedit/:no", element: <BoardEdit />},
    {path: "*", element: <NotFound />},
  ]
  return (
    <>
      <Nav />
      <Routes>
        { paths?.map((v, i) => <Route key={i} path={v.path} element={v.element} />) }
      </Routes>
    </>
  )
}

export default App
