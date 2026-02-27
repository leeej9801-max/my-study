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

# 2. SSH key 사용하기

- key 생성
```bash
ssh-keygen -t ed25519
```

- 공개키 이름 만들기
```bash
cp .ssh/id_ed25519.pub authorized_keys
```

- Container `.ssh` 폴더 준비
```bash
mkdir ~/.ssh
chmod 700 ~/.ssh
```

- Container 복사
```bash
docker cp ./authorized_keys os:/home/study/.ssh/authorized_keys
```

- 파일 소유권 설정
```bash
chown -R study:study /home/study/.ssh
```
