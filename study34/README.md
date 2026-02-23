## 1. Ubuntu 설치

- ubuntu 이미지 받기
```bash
docker pull ubuntu:24.04
```

- ubuntu 컨테이너 생성 후 접속
```bash
docker run -it -p 22:22 --name os ubuntu:24.04 /bin/bash
```

- package 최신화 하기
```bash
apt update
```

- openssh-server 설치
```bash
apt install -y openssh-server
```

- SSH 서비스 상태 확인
```bash
service ssh status
```

- SSH 프로세스 확인
```bash
ps -ef | grep sshd
```
