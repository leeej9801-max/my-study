import { useNavigate } from "react-router"
import { useState } from "react"
import Input from "./Input.jsx"
import Radio from "./Radio.jsx"
import Bottons from "./Bottons.jsx"

const Create = () => {
  const navigate = useNavigate()
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [pwd, setPwd] = useState("")
  const [gender, setGender] = useState(true)
  const close = () => navigate("/")
  const getDate = () => {
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const day = String(now.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }
  const onSubmit = e => {
    e.preventDefault()
    const data = {name, email, pwd, gender, regDate: getDate()}
    console.log(data)
  }
  return (
    <div className="container mt-3">
      <h1 className="display-1 text-center">사용자 등록</h1>
      <form onSubmit={onSubmit}>
        <Input id="name" name="이름" type="text" placeholder="이름을 입력하세요." readonly={false} value={name} onChange={setName} />
        <Input id="email" name="이메일" type="email" placeholder="이메일를 입력하세요." readonly={false} value={email} onChange={setEmail} />
        <Input id="pwd" name="비밀번호" type="password" placeholder="비밀번호를 입력하세요." readonly={false} value={pwd} onChange={setPwd} />
        <Radio readonly={false} gender={gender} onChange={setGender}/>
        <Bottons close={close} btn1={false} btn2={false} btn3={true} btn4={true} />
      </form>
    </div>
  )
}

export default Create