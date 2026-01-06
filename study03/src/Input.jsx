const Input = ({id, name, type, placeholder, readonly, value, onChange}) => {
  return (
    <div className="mb-3 mt-3">
      <label htmlFor={id} className="form-label">{name}:</label>
      <input type={type} className="form-control" id={id} name={id} placeholder={placeholder} readOnly={readonly} value={value} onChange={e=>onChange(e.target.value)} />
    </div>
  )
}

export default Input