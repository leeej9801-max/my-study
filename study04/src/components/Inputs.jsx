import { useState } from "react"

const Input = ({props}) => {
  const [data, setData] = useState(props?.value)
  const event = e => {
    setData(e.target.value)
    props?.onChange(e.target.value)
  }
  return (
    <div className="mb-3 mt-3">
      <label htmlFor={props?.id} className="form-label">{props?.name}:</label>
      <input type={props?.type} className="form-control" id={props?.id} name={props?.id} placeholder={props?.placeholder} readOnly={props?.readonly} required={props?.required} value={data} onChange={event} />
    </div>
  )
}

const Inputs = props => {
  return (
    props?.inputs?.map((v, i) => <Input key={i} props={v} />)
  )
}

export default Inputs