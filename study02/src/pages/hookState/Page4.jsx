import { useState } from "react"
import { setStorage, getStorage, removeStorage } from "@utils/storage.js"

const Input = props => {
  return (
    <div className="mb-3 mt-3">
      <label htmlFor={props.id} className="form-label">{props.name}:</label>
      <input type={props.type} className="form-control" 
             id={props.id} placeholder={props.desc} 
             name={props.id} required={props.required}
             onChange={e=> props.onChange(e.target.value)}/>
    </div>
  )
}
const Gender = props => {
  const event = e => props.checkBoolean(e.target.value)
  return (
    <div className="d-flex">
      <div className="p-2 flex-fill">
        <div className="form-check">
        <input type="radio" className="form-check-input" id="gender1" name={props.id} value="1" checked={props.gender} onChange={event}/>남성
        <label className="form-check-label" htmlFor="gender1"></label>
      </div>
      </div>
      <div className="p-2 flex-fill">
        <div className="form-check">
        <input type="radio" className="form-check-input" id="gender2" name={props.id} value="2" checked={!props.gender} onChange={event}/>여성
        <label className="form-check-label" htmlFor="gender2"></label>
      </div>
      </div>
    </div>
  )
}
const Buttons = props => {
  return (
    <div className="d-flex gap-2">
      <div className="flex-fill d-grid">
        <button type="submit" className="btn btn-primary">생성</button>
      </div>
      <div className="flex-fill d-grid">
        <button type="button" className="btn btn-primary">취소</button>
      </div>
    </div>
  )
}

const Page4 = () => {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [pwd, setPwd] = useState("")
  const [gender, setGender] = useState(true)
  const checkBoolean = value => setGender(value === "1" ? true : false)
  const onSubmit = e => {
    e.preventDefault()
    const data = {name, email, pwd, gender}
    console.log(data)
  }
  const arr = [
    {id: "name", name: "이름", type: "text", desc: "이름을 입력하세요.", 
     required: true, onChange: setName},
    {id: "email", name: "이메일", type: "email", desc: "이메일를 입력하세요.", 
     required: true, onChange: setEmail},
    {id: "pwd", name: "비밀번호", type: "password", desc: "비밀번호를 입력하세요.", 
     required: false, onChange: setPwd}
  ]
  return (
    <div className="container mt-3">
      <h1 className="display-1 text-center">사용자 등록</h1>
      <form onSubmit={onSubmit}>
        {
          arr.map((v, i) => <Input key={i} id={v.id} name={v.name}
               type={v.type} desc={v.desc}
               required={v.required} onChange={v.onChange} />)
        }
        <Gender gender={gender} checkBoolean={checkBoolean}/>
        <Buttons />
      </form>
    </div>
  )
}

export default Page4