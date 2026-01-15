import fs from 'fs';

const FILE_PATH = './data/memo.json';

const getData = () => {
  const f = fs.readFileSync(FILE_PATH, 'utf-8');
  return JSON.parse(f)
}

const setData = (data) => {
  fs.writeFileSync(FILE_PATH, JSON.stringify(data), 'utf-8');
  list();
}

export const list = () => {
  const data = getData();
  if(data.words.length > 0) {
    let line1 = "";
    let line2 = "";
    for(let i = 0; i < 50; i++) {
      line1 += "=";
      line2 += "-";
    }
    console.log(line1);
    console.log(`번호\t내용`);
    data.words.forEach((v, i) => {
      if(i < data.words.length) console.log(line2);
      console.log(`${v.id}\t${v.word}`);
    });
    console.log(line1);
  } else {
    console.log("데이터가 없습니다.")
  }
}

export const insert = (word) => {
  const data = getData();
  const words = data.words;
  const id = (words.length === 0) ? 1 : words.at(-1).id + 1;
  const row = {id, word};
  words.push(row);
  data.words = words;
  setData(data);
}

export const update = (id, word) => {
  const data = getData();
  const words = data.words;
  data.words = words.filter(v => {
    if(v.id === Number(id)) v.word = word;
    return v;
  });
  setData(data);
}

export const remove = (id) => {
  const data = getData();
  const words = data.words;
  data.words = words.filter(v => v.id !== Number(id));
  setData(data);
}