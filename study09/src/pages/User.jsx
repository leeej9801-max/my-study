import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router"
import Image from "@components/Image.jsx"
import { list } from "@/data.js"

const User = () => {
  const params = useParams()
  const navigate = useNavigate()
  const [user, setUser] = useState({name: "", email: "", pwd: "", job: "", gender: true})
  const onChange = e => {
    let {name, value} = e.target
    if(name === "gender") value = value === "1"
    setUser({...user, [name]: value})
  }
  const onSubmit = e => {
    e.preventDefault()
    console.log(user)
  }
  useEffect(()=> {
    const arr = list.filter(row => row.no === Number(params.no));
    if(arr.length === 0) return navigate("/");
    setUser(arr[0])
  }, [])
  return (
    <>
      <h1 className="text-center bg-success text-dark bg-opacity-50">User</h1>
      <Image check={user.gender} className="d-block mx-auto mt-3 profile-image" alt="Profile image" />
      <form onSubmit={onSubmit}>
        <div className="mb-3 mt-3">
          <label htmlFor="name">Name:</label>
          <input type="text" className="form-control" id="name" placeholder="Enter name" name="name" value={user.name} onChange={onChange} required readOnly />
        </div>
        <div className="mb-3 mt-3">
          <label htmlFor="email">Email:</label>
          <input type="email" className="form-control" id="email" placeholder="Enter email" name="email" value={user.email} onChange={onChange} required readOnly />
        </div>
        <div className="mb-3">
          <label htmlFor="pwd">Password:</label>
          <input type="password" className="form-control" id="pwd" placeholder="Enter password" name="pwd" value={user.pwd} onChange={onChange} required readOnly />
        </div>
        <div className="mb-3">
          <label htmlFor="job">Job:</label>
          <input type="text" className="form-control" id="job" placeholder="Enter job" name="job" value={user.job} onChange={onChange} />
        </div>
        <div className="d-flex">
          <div className="p-2 flex-fill">
            <div className="form-check">
            <input type="radio" className="form-check-input" id="gender1" name="gender" value="1" checked={user.gender} readOnly onChange={onChange} />남성
            <label className="form-check-label" htmlFor="gender1"></label>
          </div>
          </div>
          <div className="p-2 flex-fill">
            <div className="form-check">
            <input type="radio" className="form-check-input" id="gender2" name="gender" value="2" checked={!user.gender} readOnly onChange={onChange} />여성
            <label className="form-check-label" htmlFor="gender2"></label>
          </div>
          </div>
        </div>
        <div className="d-flex">
          <div className="p-2 flex-fill d-grid">
            <button type="submit" className="btn btn-success">Edit</button>
          </div>
          <div className="p-2 flex-fill d-grid">
            <a href="/" className="btn btn-danger">Cancel</a>
          </div>
        </div>
      </form>
    </>
  )
}

export default User