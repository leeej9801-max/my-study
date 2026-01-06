import { useNavigate, useParams } from "react-router";
import { useState, useEffect } from "react";
import Inputs from "@components/Inputs.jsx";
import Radio from "@components/Radio.jsx";
import Buttons from "@components/Buttons.jsx";
import { getStorage, setStorage } from "@utils/storage.js";

const Select = () => {
  const params = useParams();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [pwd, setPwd] = useState("");
  const [gender, setGender] = useState(true);
  const [inputs, setInputs] = useState([]);
  const [btns, setBtns] = useState([]);
  const [list, setList] = useState([])
  const update = () => navigate(`/edit/${params.id}`)
  const onSubmit = (e) => {
    e.preventDefault();
    const newList = list.filter((_, i) => i !== Number(params.id));
    setStorage("list", newList);
    navigate("/");
  }
  const close = () => navigate("/");
  const init = user => {
    setName(user?.name);
    setEmail(user?.email);
    setPwd(user?.pwd);
    setGender(user?.gender);
    const arr1 = [
      {id: "name", name: "이름", type: "text", placeholder: "이름을 입력하세요.", readonly: true, required: true, value: user?.name, onChange: setName },
      {id: "email", name: "이메일", type: "email", placeholder: "이메일를 입력하세요.", readonly: true, required: true, value: user?.email, onChange: setEmail },
      {id: "pwd", name: "비밀번호", type: "password", placeholder: "비밀번호를 입력하세요.", readonly: true, required: false, value: user?.pwd, onChange: setPwd },
    ]
    setInputs(arr1)
    const arr2 = [
      {type: "button", txt: "수정", onclick: update},
      {type: "submit", txt: "삭제", onclick: null},
      {type: "button", txt: "취소", onclick: close},
    ]
    setBtns(arr2)
  }
  useEffect(() => {
    const allList = getStorage("list")
    if(allList !== null) {
      setList(allList)
      const user = allList[params.id]
      if(user === undefined) {
        close();
        return;
      }
      init(allList[params.id])
    } else {
      close();
      return;
    }
  }, [])
  return (
    <div className="container mt-3">
      <h1 className="display-1 text-center">사용자 정보</h1>
      <form onSubmit={onSubmit}>
        <Inputs inputs={inputs} />
        <Radio readonly={true} gender={gender} onChange={null} />
        <Buttons btns={btns} />
      </form>
    </div>
  );
};

export default Select;
