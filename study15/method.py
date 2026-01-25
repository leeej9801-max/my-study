from db import findOne, findAll, save

def empty():
  print("함수 정의가 되어 있지 않습니다.")

def select(args):
  sql = """
        SELECT `id`, 
               `word`, 
               DATE_FORMAT(`regDate`, '%Y-%m-%d %H:%i:%s') AS regDate
        FROM edu.study
        """
  list = findAll(sql)
  print(f"번호\t글자\t생성일자")
  print("-"*50)
  for row in list:
    print(f"{row["id"]}\t{row["word"]}\t{row["regDate"]}")
  sql = """ 
        SELECT `id`, 
               `word`, 
               DATE_FORMAT(`regDate`, '%Y-%m-%d %H:%i:%s') AS regDate
        FROM edu.study
        WHERE `id` = 2
      """
  row = findOne(sql)
  print(f"{row["id"]}\t{row["word"]}\t{row["regDate"]}")

def insert(args):
  sql = f"INSERT INTO edu.study (`word`) VALUE ('{args.word}')"
  save(sql)
  select(None)

def update(args):
  sql = f"UPDATE edu.study SET `word` = '{args.word}' WHERE `id` = {args.id}"
  save(sql)
  select(None)

def delete(args):
  sql = f"DELETE FROM edu.study WHERE `id` = {args.id}"
  save(sql)
  select(None)
