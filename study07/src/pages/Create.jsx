import { useState } from "react"
import { useNavigate } from "react-router"

const Create = () => {
  const navigate = useNavigate()
  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")
  const [accept, setAccept] = useState(0)
  const close = () => navigate("/")
  const onSubmit = e => {
    e.preventDefault()
    const data = {title, content, accept}
    console.log(data)
    close()
  }
  return (
    <>
      <h1 className="text-center bg-success text-dark bg-opacity-50">CREATE</h1>
      <form onSubmit={onSubmit}>
        <div className="mb-3 mt-3">
          <label htmlFor="title" className="form-label">Title:</label>
          <input type="text" className="form-control" id="title" placeholder="Enter title" name="title" required autoComplete="off" value={title} onChange={e=>setTitle(e.target.value)} />
        </div>
        <div className="mb-3">
          <label htmlFor="content" className="form-label">Content:</label>
          <input type="text" className="form-control" id="content" placeholder="Enter content" name="content" autoComplete="off" value={content} onChange={e=>setContent(e.target.value)} />
        </div>
        <div className="d-grid gap-2 d-md-flex justify-content-md-end">
          <button className="btn btn-primary me-md-2" type="submit">생성</button>
          <button className="btn btn-warning" type="button" onClick={close}>취소</button>
        </div>
      </form>
    </>
  )
}

export default Create