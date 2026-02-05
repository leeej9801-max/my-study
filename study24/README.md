## Nginx 다운로드
```bash
docker pull nginx:1.28
```

## 컨테이너 생성
```bash
docker run --network=my-net -d -p 80:80 --name web nginx:1.28
```

### `docker run` 옵션
```
-i          : 컨터이너와 상호 입출력 활성화 정의
-t          : tty 활성화. 주로 -i 옵션과 함께 이용
-it         : -i와 -t를 한번에 정의하는 옵션

-p          : 포트포워딩 옵션   (ex 로컬포트:컨테이너포트)

-e          : 환경변수를 지정하거나 값을 변경 하는 옵션

-v          : 저장소 연경 또는 공유 하는 옵션
> 도커의 저장소 (도커 내부의 `Volumes` 영역 공간)
> 로컬의 저장소 (컴퓨터의 HDD 또는 SSD)
```

## ping 알아보기
```bash
apt install -y iputils-ping
```

## Nginx 화면 경로
```bash
/usr/share/nginx/html/index.html
```

## Dockerfile 설명
```
FROM        : 기본 대상 이미지를 정의 하는 속성

MAINTAINER  : 작성자의 정보를 기록하는 속성

RUN         : FROM의 기반 이미지 위에서 실행될 명령어 정의

COPY        : 도커 컨테이너의 경로로 파일을 복사 할때 사용하는 속성
COPY 로컬:컨테이너 
COPY ./index.html:/usr/share/nginx/html/index.html

ENV         : 도커 컨테이너의 환경변수를 정의 하는 속성

EXPOSE      : 연결할 포트 번호 정의

ENTRYPOINT  : 도커 컨테이너 생성 후 실행될 명령어 (1회 실행)

CMD         : 도커 컨테이너 시작 이후 실행될 명령어
```