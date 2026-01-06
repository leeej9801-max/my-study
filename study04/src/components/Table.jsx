const Table = ({list, styles, onClick}) => {
  return (
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
          list.map((v,i) => {
            return (
              <tr key={i} style={styles} onClick={()=>onClick(i)}>
                <td>{v.name}</td>
                <td>{v.email}</td>
                <td>{v.regDate}</td>
              </tr>
            )
          })
        }          
      </tbody>
    </table>
  )
}

export default Table