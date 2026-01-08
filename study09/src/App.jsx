import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { BrowserRouter, Routes, Route } from "react-router";
import "@/style.css";
import Nav from "@components/Nav.jsx";
import Footer from "@components/Footer.jsx";
import Main from "@pages/Main.jsx";
import SignIn from "@pages/SignIn.jsx";
import SignUp from "@pages/SignUp.jsx";
import User from "@pages/User.jsx";
import NotFound from "@pages/NotFound.jsx";

const App = () => {
  const paths = [
    {path: "/", element: <Main />},
    {path: "/signIn", element: <SignIn />},
    {path: "/signUp", element: <SignUp />},
    {path: "/user/:no", element: <User />},
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
