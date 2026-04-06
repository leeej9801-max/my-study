const Radio = ({readonly, gender, onChange}) => {
  const checkBoolean = e => {
    if(!readonly) {
      if(e.target.value === "1") {
        onChange(true)
      } else {
        onChange(false)
      }
    }
  }
  return (
    <div className="d-flex">
      <div className="p-2 flex-fill">
        <div className="form-check">
        <input type="radio" className="form-check-input" id="radio1" name="optradio" value="1" checked={gender} readOnly={readonly} onChange={checkBoolean} />남성
        <label className="form-check-label" htmlFor="radio1"></label>
      </div>
      </div>
      <div className="p-2 flex-fill">
        <div className="form-check">
        <input type="radio" className="form-check-input" id="radio2" name="optradio" value="2" checked={!gender} readOnly={readonly} onChange={checkBoolean} />여성
        <label className="form-check-label" htmlFor="radio2"></label>
      </div>
      </div>
    </div>
  )
}

export default Radio