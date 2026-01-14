# 변수
a = 1
print(a, type(a))

# 자료형
print(type(1))
print(type(1.0))
print(type(""))   # 편집과 특정 값 가져오기
print(type(True))
print(type(None))
print(type({}))
print(type([]))
print(type(()))

# 함수 생성
def fn():
  print("fn()")

# 함수 사용(요청)
fn()

# 클래스 선언
class Aclass:
  def __init__(self):
    pass
  def add(self, a, b):
    return a + b

# 클래스 생성(인스턴스 생성)
ac = Aclass()
print(ac.add(2,5))

# 제어문
# 조건문 (if, else, elif)
if 5 > 1: 
  print("5가 크다")
elif 5 < 1:
  pass
else:
  pass

# 반복문 (for) range(0) [] () ""
for i in "": # 값
  print(i)

arr = [1,2,3,4,5]
for i in range(len(arr)): # 인덱스 0, 1, 2, 3, 4
  print(i, arr[i])

arr = [[1,2],[1],[1,2,3]]
for y in range(len(arr)): # 인덱스
  for x in range(len(arr[y])): # 인덱스
    print(y, x, arr[y][x])

문자열 = "나는 한국인일까?"
print(문자열[:3])

arr1 = {}
arr2 = dict() # 형변환 함수
print(type(arr1), type(arr2))

print(type(int("1")))

print(10 == int("10")) # 참

obj = {}
obj["key"] = 10
print(obj, type(obj))

arr = [0]
arr[0] = 10
print(arr, type(arr))

arr = list()
arr.append(10)
print(arr, type(arr))
arr[0] = 20
print(arr, type(arr))

t = (1,2)
arr = list(t)
arr.append(10)
t = tuple(arr)
print(type(t), t)

arr2 = set(t)
arr3 = set(arr)
print(arr2 | arr3)