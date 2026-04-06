import { useState } from "react"
import { list } from "@/data.js"

const SignIn = () => {
  const [user, setUser] = useState({email: "", pwd: ""})
  const onChange = e => {
    const {name, value} = e.target
    setUser({...user, [name]: value})
  }
  const onSubmit = e => {
    e.preventDefault()
    const arr = list.filter(row => (row.email === user.email && row.pwd === user.pwd));
    if(arr.length > 0) {
      console.log(`${arr[0].name} 님 환영합니다.`)
    } else {
      console.log("로그인 실패 하였습니다.")
    }
  }
  return (
    <>
      <h1 className="text-center bg-success text-dark bg-opacity-50">SignIn</h1>
      <form onSubmit={onSubmit}>
        <div className="mb-3 mt-3">
          <label htmlFor="email">Email:</label>
          <input type="email" className="form-control" id="email" placeholder="Enter email" name="email" value={user.email} onChange={onChange} required />
        </div>
        <div className="mb-3">
          <label htmlFor="pwd">Password:</label>
          <input type="password" className="form-control" id="pwd" placeholder="Enter password" name="pwd" value={user.pwd} onChange={onChange} required />
        </div>
        <div className="d-flex">
          <div className="p-2 flex-fill d-grid">
            <button type="submit" className="btn btn-warning">SignIn</button>
          </div>
          <div className="p-2 flex-fill d-grid">
            <a href="/signUp" className="btn btn-primary">SignUp</a>
          </div>
          <div className="p-2 flex-fill d-grid">
            <a href="/" className="btn btn-danger">Cancel</a>
          </div>
        </div>
      </form>
    </>
  )
}

export default SignIn