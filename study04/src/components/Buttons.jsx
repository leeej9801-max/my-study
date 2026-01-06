const Button = ({props}) => {
  return (
    <div className="p-2 flex-fill d-grid">
      <button type={props.type} className="btn btn-primary" onClick={props.onclick}>{props.txt}</button>
    </div>
  )
}

const Buttons = props => {
  return (
    <div className="d-flex">
      {
        props?.btns?.map((v,i) => <Button key={i} props={v} />)
      }
    </div>
  )
}

export default Buttons