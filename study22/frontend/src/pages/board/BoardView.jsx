import { useState , useEffect } from 'react' 
import { useNavigate, useParams } from "react-router";
import { api } from '@utils/network.js'

const BoardView = () => {
  const [no, setNo] = useState(0)
  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")
  const [name, setName] = useState("")
  const [role, setRole] = useState(false)
  const params = useParams();
  const navigate = useNavigate()
  const deleteEvent = () => {
    api.delete(`/board/${params.no}`)
    .then(res=>{
      alert(res.data.message)
      if(res.data.status) navigate("/")
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
    api.post(`/board/${params.no}`)
    .then(res=>{
      if(res.data.status) {
        //const data = { "no": 1, "title": "샘플을 만들었어요", "content": "내용을 작성해 주세요.", "name": "이나라" }
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
			<h1 className="display-1 text-center">게시글 상세</h1>
			<form>
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
					<textarea type="text" className="form-control h-50" rows="10" id="content" name="content" readOnly="readonly" defaultValue={content}></textarea>
				</div>
			</form>
			<div className="d-flex">
        {role &&
        <>
          <div className="p-2 flex-fill d-grid">
            <button type="button" className="btn btn-primary" onClick={()=>navigate(`/boardedit/${no}`)}>수정</button>
          </div>
          <div className="p-2 flex-fill d-grid">
            <button type="button" className="btn btn-primary" onClick={deleteEvent}>삭제</button>
          </div>
        </>}
        <div className="p-2 flex-fill d-grid">
          <button type="button" className="btn btn-primary" onClick={()=>navigate("/")}>취소</button>
        </div>
			</div>
		</div>
  )
}

export default BoardView