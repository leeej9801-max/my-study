import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { BrowserRouter, Routes, Route } from "react-router";
import List from "./List.jsx"
import Select from "./Select.jsx"
import Create from "./Create.jsx"

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<List />} />
        <Route path='/detail' element={<Select />} />
        <Route path='/new' element={<Create />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
