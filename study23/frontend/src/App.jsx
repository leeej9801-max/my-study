import axios from 'axios'

const NotFound = () => {
  return (
    <div className="text-center">
      <h1>404</h1>
      <p>페이지를 찾을 수 없습니다.</p>
    </div>
  )
}

const App = () => {
  const btnEvent = () => {
    const baseURL = import.meta.env.VITE_APP_FASTAPI_URL || "http://localhost:8000"
    axios.get(`${baseURL}/`)
    .then(res=>console.log(res))
    .catch(err => console.error(err))
  }
  return (
    <>
    <button type='button' className='btn' onClick={btnEvent}>확인</button>
    <NotFound />
    </>
  )
}

export default App
