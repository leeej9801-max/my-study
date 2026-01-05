import { useLocation, useNavigate } from "react-router"
import { useState, useEffect } from "react"
import Input from "./Input.jsx"
import Radio from "./Radio.jsx"
import Bottons from "./Bottons.jsx"

const Select = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [pwd, setPwd] = useState("")
  const [gender, setGender] = useState(true)
  const close = () => navigate("/")
  useEffect(() => {
    if(location.state === null) {
      close()
      return
    }
    const data = location.state
    setName(data.name)
    setEmail(data.email)
    setPwd(data.pwd)
    setGender(data.gender)
  }, [])
  return (
    <div className="container mt-3">
      <h1 className="display-1 text-center">사용자 정보</h1>
      <form>
        <Input id="name" name="이름" type="text" placeholder="이름을 입력하세요." readonly={true} value={name} onChange={setName} />
        <Input id="email" name="이메일" type="email" placeholder="이메일를 입력하세요." readonly={true} value={email} onChange={setEmail} />
        <Input id="pwd" name="비밀번호" type="password" placeholder="비밀번호를 입력하세요." readonly={true} value={pwd} onChange={setPwd} />
        <Radio readonly={true} gender={gender} onChange={setGender}/>
        <Bottons close={close} btn1={true} btn2={true} btn3={false} btn4={true} />
      </form>
    </div>
  )
}

export default Select