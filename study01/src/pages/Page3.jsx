import { useState } from 'react'
import { useNavigate } from 'react-router'

const Page3 = () => {
  const navigate =  useNavigate()
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [pwd, setPwd] = useState("")
  const [gender, setGender] = useState(true)
  const onclick = () => navigate("/")
  const onSubmit = e => {
    e.preventDefault()
    const data = {name, email, pwd, gender}
    console.log(data)
  }
  return (
    <div className="container mt-3">
      <h1 className="display-1 text-center">사용자 정보</h1>
      <form onSubmit={onSubmit}>
        <div className="mb-3 mt-3">
          <label htmlFor="name" className="form-label">이름:</label>
          <input type="text" className="form-control" id="name" placeholder="이름을 입력하세요." name="name" value={name} onChange={e=>setName(e.target.value)} />
        </div>
        <div className="mb-3 mt-3">
          <label htmlFor="email" className="form-label">이메일:</label>
          <input type="email" className="form-control" id="email" placeholder="이메일를 입력하세요." name="email" value={email} onChange={e=>setEmail(e.target.value)} />
        </div>
        <div className="mb-3">
          <label htmlFor="pwd" className="form-label">비밀번호:</label>
          <input type="password" className="form-control" id="pwd" placeholder="비밀번호를 입력하세요." name="pwd" value={pwd} onChange={e=>setPwd(e.target.value)} />
        </div>
        <div className="d-flex">
          <div className="p-2 flex-fill">
            <div className="form-check">
            <input type="radio" className="form-check-input" id="radio1" name="gender" value="1" checked={gender === true} onChange={e=>setGender(true)} />남성
            <label className="form-check-label" htmlFor="radio1"></label>
          </div>
          </div>
          <div className="p-2 flex-fill">
            <div className="form-check">
            <input type="radio" className="form-check-input" id="radio2" name="gender" value="2" checked={gender === false} onChange={e=>setGender(false)} />여성
            <label className="form-check-label" htmlFor="radio2"></label>
          </div>
          </div>
        </div>
        <div className="d-flex">
          <div className="p-2 flex-fill d-grid">
            <button type='submit' className="btn btn-primary">생성</button>
          </div>
          <div className="p-2 flex-fill d-grid">
            <button type='button' className="btn btn-primary" onClick={onclick}>취소</button>
          </div>
        </div>
      </form>
    </div>
  )
}

export default Page3