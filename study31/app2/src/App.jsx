import axios from 'axios'

const App = () => {
  const event1 = e => {
    e.preventDefault()
    const fileList = e.target.file.files
    const formData = new FormData();
    formData.append("txt", e.target.txt.value)
    for(let i = 0; i < fileList.length; i++) {
      formData.append("files", fileList[i])
    }
    axios.post("http://localhost:8000/upload", formData, 
      {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
    )
    .then(res=>console.log(res))
    .catch(err=>console.error(err))
  }
  const event2 = async e => {
    e.preventDefault()
    const fileList = e.target.file.files
    const txt = e.target.txt.value
    const files = []
    for(let i = 0; i < fileList.length; i++) {
      const file = fileList[i]
      const base64File = await fileToBase64(file)
      files[i] = base64File
    }
    const params = { txt, files }
    axios.post("http://localhost:8000/upload2", params)
    .then(res=>console.log(res))
    .catch(err=>console.error(err))
  }
  const fileToBase64 = file => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file)

      reader.onload = () => {
        const data = reader.result.split(",")[1]
        resolve(data)
      }

      reader.onerror = err => {
        console.error(err)
        reject(err)
      }
    })
  }
  return (
    <>
      <header>
        <h1>File Upload</h1>
      </header>
      <main>
        <form onSubmit={event2}>
          <div className="form">
            <input type="text" name="txt" id="txt" />
          </div>
          <div className="form">
            <input type="file" name="file" id="file1" multiple accept="image/*" />
          </div>
          <div className="form">
            <input type="submit" value="파일업로드" />
          </div>
        </form>
      </main>
    </>
  )
}

export default App
