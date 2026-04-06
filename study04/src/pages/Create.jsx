import { useNavigate } from "react-router";
import { useState, useEffect } from "react";
import Inputs from "@components/Inputs.jsx";
import Radio from "@components/Radio.jsx";
import Buttons from "@components/Buttons.jsx";
import { getStorage, setStorage, getDate } from "@utils/storage.js";

const Create = () => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [pwd, setPwd] = useState("");
  const [gender, setGender] = useState(true);
  const [inputs, setInputs] = useState([]);
  const [btns, setBtns] = useState([]);
  const [list, setList] = useState([])
  const close = () => navigate("/");
  const onSubmit = (e) => {
    e.preventDefault();
    const data = { name, email, pwd, gender, regDate: getDate() };
    setStorage("list", [...list, data])
    close()
  };
  useEffect( ()=>{
    const arr1 = [
      {id: "name", name: "이름", type: "text", placeholder: "이름을 입력하세요.", readonly: false, required: true, value: name, onChange: setName },
      {id: "email", name: "이메일", type: "email", placeholder: "이메일를 입력하세요.", readonly: false, required: true, value: email, onChange: setEmail },
      {id: "pwd", name: "비밀번호", type: "password", placeholder: "비밀번호를 입력하세요.", readonly: false, required: false, value: pwd, onChange: setPwd },
    ]
    setInputs(arr1)
    const arr2 = [
      {type: "submit", txt: "생성", onclick: null},
      {type: "button", txt: "취소", onclick: close},
    ]
    setBtns(arr2)
    const data = getStorage("list")
    if(data !== null) setList(data)
  }, [])
  return (
    <div className="container mt-3">
      <h1 className="display-1 text-center">사용자 등록</h1>
      <form onSubmit={onSubmit}>
        <Inputs inputs={inputs} />
        <Radio readonly={false} gender={gender} onChange={setGender} />
        <Buttons btns={btns} />
      </form>
    </div>
  );
};

export default Create;
