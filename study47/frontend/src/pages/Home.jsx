import { useState, useEffect } from 'react'
import { api } from '@utils/network.js'

const Home = () => {
  const [list, setList] = useState([])
  const [item, setItem] = useState({email: "", content: ""})
  const [mode, setMode] = useState(false)
  const eventSubmit = e => {
    e.preventDefault()

    // api.post("/webhook-test/app", item)
    api.get("/webhook/app")
    .then(res => {
      // console.log(res)
      if(res.data.status) {
        setItem({email: "", content: ""})
        setList(res.data.result)
      }
    })
    .catch(err => console.log(err));

  }
  const setChange = e => {
    setItem({...item, [e.target.name]: e.target.value})
  }
  const eventClick = v => {
    setMode(!mode)
  }
  useEffect(() => {
    
  }, [])
  return (
    <div className="container mt-3">
			<h1 className="display-1 text-center">n8n</h1>
      <form onSubmit={eventSubmit}>
        <div className="mb-3">
          <select className="form-select" defaultValue="" placeholder="HTTP METHOD">
            <option value="1">GET</option>
            <option value="2">POST</option>
            <option value="3">PUT</option>
            <option value="3">DELETE</option>
          </select>
        </div>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email</label>
          <input type="email" className="form-control" name="email" id="email" required placeholder="name@example.com" value={item.email} onChange={setChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="content" className="form-label">Content</label>
          <textarea className="form-control" name="content" id="content" rows="3" onChange={setChange} value={item.content}></textarea>
        </div>
        <div className="btn-group w-100">
          <button type="submit" className="btn btn-primary" disabled={mode}>추가</button>
          <button type="button" className="btn btn-primary" disabled={!mode}>삭제</button>
        </div>
      </form>
      <div className="list-group mt-3">
        {
          list.map((v, i) => 
            <button key={i} type="button" className="list-group-item list-group-item-action" onClick={()=>eventClick(v)}>{v.content}</button>
          )
        }
      </div>
		</div>
  )
}

export default Home