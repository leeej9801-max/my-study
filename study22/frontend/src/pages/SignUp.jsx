import { useState } from 'react'
import { useNavigate } from "react-router";
import { useAuth } from '@hooks/AuthProvider.jsx'
import { api } from '@utils/network.js'

const SignUp = () => {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [pwd, setPwd] = useState("")
  const [gender, setGender] = useState(true)
  const { setAuth } = useAuth()
  const navigate = useNavigate()
  const submitEvent = e => {
    e.preventDefault()
    const params = { name, email, pwd, gender }
    api.put("/signUp", params)
    .then(res => {
      if(res.data.status) {
        setAuth(res.data.status);
      } else {
        alert(res.data.message);
        setName("");
        setEmail("");
        setPwd("");
        setGender(true);
      }
    })
    .catch(err => console.error(err))
  }
  return (
    <div className="container mt-3">
			<h1 className="display-1 text-center">회원가입</h1>
			<form onSubmit={submitEvent}>
				<div className="mb-3 mt-3">
					<label htmlFor="name" className="form-label">이름:</label>
					<input type="text" className="form-control" id="name" placeholder="이름을 입력하세요." name="name" value={name} onChange={e=>setName(e.target.value)} autoComplete='off' required={true} />
				</div>
				<div className="mb-3 mt-3">
					<label htmlFor="email" className="form-label">이메일:</label>
					<input type="email" className="form-control" id="email" placeholder="이메일를 입력하세요." name="email" value={email} onChange={e=>setEmail(e.target.value)}  autoComplete='off' required={true} />
				</div>
				<div className="mb-3">
					<label htmlFor="pwd" className="form-label">비밀번호:</label>
					<input type="password" className="form-control" id="pwd" placeholder="비밀번호를 입력하세요." name="pwd" value={pwd} onChange={e=>setPwd(e.target.value)}  autoComplete='off' required={true} />
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
          <div className="p-2 flex-fill d-grid">
            <button type="submit" className="btn btn-primary">가입</button>
          </div>
          <div className="p-2 flex-fill d-grid">
            <button type="button" className="btn btn-primary" onClick={()=>navigate("/")}>취소</button>
          </div>
        </div>
			</form>
		</div>
  )
}

export default SignUp