import fs from 'fs';

const getData = () => {
  const f = fs.readFileSync('./data/memo.json', 'utf-8');
  return JSON.parse(f)
  return data.list
}

export const add = (a, b) => {
  const data = getData();
  const result = Number(a) + Number(b)
  data.list.push(result)
  console.log(data, result);
  fs.writeFileSync('./data/memo.json', JSON.stringify(data), 'utf-8')
}

export const list = () => {
  console.log("list() 호출됨");
  const arr = getData().list;
  for(const v of arr) console.log(v);
}