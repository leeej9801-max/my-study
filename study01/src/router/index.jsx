// import { createBrowserRouter } from "react-router";
// import { RouterProvider } from "react-router/dom";
import { BrowserRouter, Routes, Route } from "react-router";
import Page1 from '@pages/Page1.jsx'
import Page2 from '@pages/Page2.jsx'
import Page3 from '@pages/Page3.jsx'

const Router = () => {
  // const router = createBrowserRouter([
    // { path: "/", Component: Page1 },
    // { path: "/page2", Component: Page2 },
  // ]);
  // return <RouterProvider router={router} />
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Page1 />} />
        <Route path="/page2" element={<Page2 />} />
        <Route path="/page3" element={<Page3 />} />
      </Routes>
    </BrowserRouter>
  )
}

export default Router