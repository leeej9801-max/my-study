import { useState } from "react"
const Page2 = () => {
  const [num, setNum] = useState(0)
  const event = () => setNum(num + 1)
  return (
    <>
      <span style={{margin: '0 10px'}}>번호 : {num}</span>
      <button type='button' 
              style={{cursor: 'pointer'}} 
              onClick={event}>상태값 변경</button>
    </>
  )
}

export default Page2