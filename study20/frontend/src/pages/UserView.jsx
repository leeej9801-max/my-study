import { useState, useEffect } from 'react'
import { useNavigate } from "react-router";
import { useAuth } from '@hooks/AuthProvider.jsx'
import { api } from '@utils/network.js'

const UserView = () => {
  const [no, setNo] = useState(0)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [pwd, setPwd] = useState("")
  const [gender, setGender] = useState(true)
  const [regDate, setRegDate] = useState("")
  const [modDate, setModDate] = useState("")
  const { clearAuth } = useAuth()
  const navigate = useNavigate()
  const deleteEvent = () => {
    alert("정상적으로 탈퇴 처리가 되었습니다.")
    clearAuth()
  }
  const setData = data => {
    setNo(data.no)
    setName(data.name)
    setEmail(data.email)
    setPwd(data.pwd)
    setGender(data.gender)
    setRegDate(data.regDate)
    setModDate(data.modDate)
  }
  useEffect(()=>{
    const result = {
      "no": 1, "name": "홍길동", "email": "hong@email.com", "pwd": "1234", "gender": true, "regDate": "2026-01-30", "modDate": "2026-01-30"
    }
    setData(result)
  }, [])
  return (
    <div className="container mt-3">
			<h1 className="display-1 text-center">회원정보</h1>
			<form>
				<div className="mb-3 mt-3">
					<label htmlFor="name" className="form-label">이름</label>
					<input type="text" className="form-control" id="name" name="name" readOnly="readonly" defaultValue={name} />
				</div>
				<div className="mb-3 mt-3">
					<label htmlFor="email" className="form-label">이메일</label>
					<input type="email" className="form-control" id="email" name="email" readOnly="readonly" defaultValue={email} />
				</div>
				<div className="mb-3">
					<label htmlFor="pwd" className="form-label">비밀번호</label>
					<input type="password" className="form-control" id="pwd" name="pwd" readOnly="readonly" defaultValue={pwd} />
				</div>
				<div className="mb-3 mt-3">
					<label htmlFor="regDate" className="form-label">가입일</label>
					<input type="text" className="form-control" id="regDate" name="regDate" readOnly="readonly" defaultValue={regDate} />
				</div>
				<div className="mb-3 mt-3">
					<label htmlFor="modDate" className="form-label">회원정보 수정일</label>
					<input type="text" className="form-control" id="modDate" name="modDate" readOnly="readonly" defaultValue={modDate} />
				</div>
				<div className="d-flex">
					<div className="p-2 flex-fill">
						<div className="form-check">
							<input type="radio" className="form-check-input" id="radio1" name="gender" value="1" checked={gender} disabled />남성
							<label className="form-check-label" htmlFor="radio1"></label>
						</div>
					</div>
					<div className="p-2 flex-fill">
						<div className="form-check">
							<input type="radio" className="form-check-input" id="radio2" name="gender" value="2" checked={!gender} disabled />여성
							<label className="form-check-label" htmlFor="radio2"></label>
						</div>
					</div>
				</div>
        <div className="d-flex">
          <div className="p-2 flex-fill d-grid">
            <button type="button" className="btn btn-primary" onClick={()=>navigate("/")}>취소</button>
          </div>
          <div className="p-2 flex-fill d-grid">
            <button type="button" className="btn btn-primary" onClick={()=>navigate("/useredit")}>수정</button>
          </div>
          <div className="p-2 flex-fill d-grid">
            <button type="button" className="btn btn-primary" onClick={deleteEvent}>탈퇴</button>
          </div>
        </div>
			</form>
		</div>
  )
}

export default UserView