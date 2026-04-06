import { useState , useEffect } from 'react' 
import { useNavigate, useParams } from "react-router";
import { api } from '@utils/network.js'
import { useAuth } from '@hooks/AuthProvider.jsx'

const BoardEdit = () => {
  const [no, setNo] = useState(0)
  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")
  const [name, setName] = useState("")
  const [role, setRole] = useState(false)
  const params = useParams();
  const navigate = useNavigate()
  const { checkAuth } = useAuth()
  const submitEvent = e => {
    e.preventDefault()
    const params = { content }
    api.patch(`/board/${no}`, params)
    .then(res=>{
      alert(res.data.message)
      if(res.data.status) navigate(`/boardview/${no}`)
    })
    .catch(err => console.error(err))
  }
  const setData = data => {
    setNo(data.no)
    setTitle(data.title)
    setContent(data.content)
    setName(data.name)
  }
  useEffect(()=>{
    if(!checkAuth()) navigate("/")
    api.post(`/board/${params.no}`)
    .then(res=>{
      if(res.data.status) {
        setData(res.data.result)
        setRole(res.data.role)
      } else {
        alert(res.data.message);
        navigate("/");
      }
    })
    .catch(err => console.error(err))
  }, [])
  return (
    <div className="container mt-3">
			<h1 className="display-1 text-center">게시글 수정</h1>
			<form onSubmit={submitEvent}>
				<div className="mb-3 mt-3">
					<label htmlFor="title" className="form-label">제목</label>
					<input type="text" className="form-control" id="title" name="title" readOnly="readonly" defaultValue={title} />
				</div>
				<div className="mb-3 mt-3">
					<label htmlFor="name" className="form-label">작성자</label>
					<input type="text" className="form-control" id="name" name="name" readOnly="readonly" defaultValue={name} />
				</div>
				<div className="mb-3 mt-3">
					<label htmlFor="content" className="form-label">내용</label>
					<textarea type="text" className="form-control h-50" rows="10" id="content" name="content" value={content} onChange={e=>setContent(e.target.value)}></textarea>
				</div>
        <div className="d-flex">
          {role &&
          <div className="p-2 flex-fill d-grid">
            <button type="submit" className="btn btn-primary">저장</button>
          </div>
          }
          <div className="p-2 flex-fill d-grid">
            <button type="button" className="btn btn-primary" onClick={()=>navigate(`/boardview/${no}`)}>취소</button>
          </div>
        </div>
			</form>
		</div>
  )
}

export default BoardEdit