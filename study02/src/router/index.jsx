import { BrowserRouter, Routes, Route } from "react-router";
import NotFound from "@pages/NotFound.jsx"
import HookState from "@pages/hookState"

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/state/*" element={<HookState />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}

export default Router