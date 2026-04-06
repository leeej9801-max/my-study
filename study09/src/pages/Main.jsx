import { list } from "@/data.js"
import Image from "@components/Image.jsx"

const Main = () => {
  return (
    <>
      <h1 className="text-center bg-success text-dark bg-opacity-50">MAIN</h1>
      <div className="btn-group">
        <a className="btn btn-warning" href="/signIn">SignIn</a>
        <a className="btn btn-primary" href="/signUp">SignUp</a>
      </div>
      <div className="row mt-2">
        {
          list?.map((v, i) => {
            return (
              <div className="col-12 col-md-6 col-lg-4 mb-3" key={v.no}>
                <div className="card">
                  <Image check={v.gender} className="card-img-top" alt="Card image" />
                  <div className="card-body">
                    <h4 className="card-title">{v.name}</h4>
                    <p className="card-text">{v.job}</p>
                    <a href={`/user/${v.no}`} className="btn btn-primary">See Profile</a>
                  </div>
                </div>
              </div>
            )
          })
        }        
      </div>
    </>
  )
}

export default Main