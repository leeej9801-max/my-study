import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { BrowserRouter, Routes, Route } from "react-router";
import List from "@pages/List.jsx";
import Select from "@pages/Select.jsx";
import Update from "@pages/Update.jsx";
import Create from "@pages/Create.jsx";
import NotFound from "@pages/NotFound.jsx";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<List />} />
        <Route path="/detail/:id" element={<Select />} />
        <Route path="/edit/:id" element={<Update />} />
        <Route path="/new" element={<Create />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
