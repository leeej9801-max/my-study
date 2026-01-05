const Bottons = ({close, btn1, btn2, btn3, btn4}) => {
  return (
    <div className="d-flex">
      {btn1 &&
        <div className="p-2 flex-fill d-grid">
          <button className="btn btn-primary">수정</button>
        </div>
      }
      {btn2 &&
        <div className="p-2 flex-fill d-grid">
          <button className="btn btn-primary">수정</button>
        </div>
      }
      {btn3 &&
        <div className="p-2 flex-fill d-grid">
          <button className="btn btn-primary">생성</button>
        </div>
      }
      {btn4 &&
        <div className="p-2 flex-fill d-grid">
          <button className="btn btn-primary" onClick={close}>취소</button>
        </div>
      }
    </div>
  )
}

export default Bottons