import { useState, useEffect } from "react"
import { useNavigate } from "react-router"
import { getStorage } from "@utils/storage.js";
import Table from "@components/Table.jsx"

const List = () => {
  const [list, setList] = useState([])
  const navigate = useNavigate()
  const styles = {cursor: "pointer"}
  const onClick = index => navigate(`/detail/${index}`)
  useEffect(()=>{
    const data = getStorage("list")
    if(data !== null) setList(data)
  }, [])
  return (
    <div className="container mt-3">
      <h1 className="display-1 text-center">사용자 목록</h1>
      <div className="btn-group">
        <a href="/new" className="btn btn-primary">사용자 추가</a>
      </div>
      <Table list={list} styles={styles} onClick={onClick} />
    </div>
  )
}

export default List
