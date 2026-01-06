import { useNavigate } from "react-router"

const List = () => {
  const navigate = useNavigate()
  const list = [
    {name: "스티븐", email: "jobs@shellfolder.com", pwd: "1234", gender: true, regDate: "2023-02-28"},
    {name: "에브릴", email: "lavigne@shellfolder.com", pwd: "567", gender: false, regDate: "2023-02-27"}
  ];
  const styles = {cursor: "pointer"}
  const onClick = data => navigate("/detail", {state: data})
  return (
    <div className="container mt-3">
      <h1 className="display-1 text-center">사용자 목록</h1>
      <div className="btn-group">
        <a href="/new" className="btn btn-primary">사용자 추가</a>
      </div>
      <table className="table table-hover mt-3">
        <thead className="table-dark">
          <tr>
            <th>이름</th>
            <th>이메일</th>
            <th>가입날짜</th>
          </tr>
        </thead>
        <tbody>
          {
            list.map((v,i) => 
            <tr key={i} style={styles} onClick={()=>onClick(v)}>
              <td>{v.name}</td>
              <td>{v.email}</td>
              <td>{v.regDate}</td>
            </tr>)
          }          
        </tbody>
      </table>
    </div>
  )
}

export default List
