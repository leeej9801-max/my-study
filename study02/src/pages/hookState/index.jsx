import { Routes, Route } from "react-router";
import { useState } from "react"
import Page1 from "@pages/hookState/Page1.jsx"
import Page2 from "@pages/hookState/Page2.jsx"
import Page3 from "@pages/hookState/Page3.jsx"
import Page4 from "@pages/hookState/Page4.jsx"
import Page5 from "@pages/hookState/Page5.jsx"

const Root = () => {
  const pages = [
    {"name": "Page1", "url": "1"},
    {"name": "Page2", "url": "2"},
    {"name": "Page3", "url": "3"},
    {"name": "Page4", "url": "4"},
    {"name": "Page5", "url": "5"},
  ]
  return (
    <div className="container mt-3">
      <h1 className="display-4 text-center">useState 알아보기</h1>
      <ul>
        {
          pages.map((v,i) => {
            return (
              <li key={i}>
                <a href={`/state/${v.url}`} target="_blank">{v.name}</a>
              </li>
            )
          })
        }
      </ul>
    </div>
  )
}

const HookState = () => {
  return (
    <Routes>
      <Route path="1" element={<Page1 />} />
      <Route path="2" element={<Page2 />} />
      <Route path="3" element={<Page3 />} />
      <Route path="4" element={<Page4 />} />
      <Route path="4" element={<Page4 />} />
      <Route path="5" element={<Page5 />} />
      <Route path="*" element={<Root />} />
    </Routes>
  )
}

export default HookState