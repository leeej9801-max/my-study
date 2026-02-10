import { useState, useEffect } from 'react'
import { useNavigate } from "react-router";
import { useAuth } from '@hooks/AuthProvider.jsx'
import { api } from '@utils/network.js'

const UserEdit = () => {
  const [no, setNo] = useState(0)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [pwd, setPwd] = useState("")
  const [gender, setGender] = useState(true)
  const [role, setRole] = useState(false)
  const { checkAuth } = useAuth()
  const navigate = useNavigate()
  const submitEvent = e => {
    e.preventDefault()
    const params = { email, pwd, gender }
    api.patch("/user", params)
    .then(res=>{
      alert(res.data.message)
      if(res.data.status) navigate("/userview")
    })
    .catch(err => console.error(err))
  }
  const setData = data => {
    setNo(data.no)
    setName(data.name)
    setEmail(data.email)
    setPwd(data.pwd)
    setGender(data.gender)
  }
  useEffect(()=>{
    if(!checkAuth()) navigate("/")
    api.post("/user")
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
			<h1 className="display-1 text-center">회원수정</h1>
			<form onSubmit={submitEvent}>
				<div className="mb-3 mt-3">
					<label htmlFor="name" className="form-label">이름</label>
					<input type="text" className="form-control" id="name" name="name" readOnly="readonly" defaultValue={name} />
				</div>
				<div className="mb-3 mt-3">
					<label htmlFor="email" className="form-label">이메일</label>
					<input type="email" className="form-control" id="email" name="email" value={email} onChange={e=>setEmail(e.target.value)}  autoComplete='off' required={true} />
				</div>
				<div className="mb-3">
					<label htmlFor="pwd" className="form-label">비밀번호</label>
					<input type="password" className="form-control" id="pwd" name="pwd" value={pwd} onChange={e=>setPwd(e.target.value)}  autoComplete='off' required={true}/>
				</div>
				<div className="d-flex">
					<div className="p-2 flex-fill">
						<div className="form-check">
							<input type="radio" className="form-check-input" id="radio1" name="gender" value="1" checked={gender} onChange={()=>setGender(true)} />남성
							<label className="form-check-label" htmlFor="radio1"></label>
						</div>
					</div>
					<div className="p-2 flex-fill">
						<div className="form-check">
							<input type="radio" className="form-check-input" id="radio2" name="gender" value="2" checked={!gender} onChange={()=>setGender(false)} />여성
							<label className="form-check-label" htmlFor="radio2"></label>
						</div>
					</div>
				</div>
        <div className="d-flex">
          {role &&
            <div className="p-2 flex-fill d-grid">
              <button type="submit" className="btn btn-primary">저장</button>
            </div>
          }
          <div className="p-2 flex-fill d-grid">
            <button type="button" className="btn btn-primary" onClick={()=>navigate("/userview")}>취소</button>
          </div>
        </div>
			</form>
		</div>
  )
}

export default UserEdit