import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { BrowserRouter, Routes, Route } from "react-router";
import Nav from "@components/Nav.jsx"
import Footer from "@components/Footer.jsx"
import NotFound from "@pages/NotFound.jsx"
import List from "@pages/List.jsx"
import Create from "@pages/Create.jsx"
import Detail from "@pages/Detail.jsx"

const App = () => {
  const paths = [
    {path: "/", element: <List />},
    {path: "/new", element: <Create />},
    {path: "/detail/:id", element: <Detail />},
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
