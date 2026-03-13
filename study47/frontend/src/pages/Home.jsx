import { useState, useEffect } from 'react'
import { api } from '@utils/network.js'

const Home = () => {
  const [list, setList] = useState([])
  const [item, setItem] = useState("")
  const searchEvent = e => {
    e.preventDefault()
    setItem("")
  }
  useEffect(() => {
    
  }, [])
  return (
    <div className="container mt-3">
			<h1 className="display-1 text-center">n8n</h1>
      <form>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email</label>
          <input type="email" class="form-control" id="email" placeholder="name@example.com" />
        </div>
        <div className="mb-3">
          <label htmlFor="content" className="form-label">Content</label>
          <textarea className="form-control" name="content" id="content" rows="3"></textarea>
        </div>
        <div className="btn-group w-100">
          <button type="button" className="btn btn-primary">추가</button>
          <button type="button" className="btn btn-primary">삭제</button>
        </div>
      </form>
      <div className="list-group mt-3">
        <button type="button" className="list-group-item list-group-item-action">Content</button>
        <button type="button" className="list-group-item list-group-item-action">Content</button>
        <button type="button" className="list-group-item list-group-item-action">Content</button>
      </div>
		</div>
  )
}

export default Home