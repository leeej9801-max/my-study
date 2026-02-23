## AWS EC2 생성하기

- `ubuntu:24:04` 이미지 선택
- 프리티어 유형 사용
- 키 페어 생성 `.pem`
- 네트워크 보안 : 22, 80 오픈
- 저장소 : `8Gb` 

## EC2 인스턴스 접속

```bash
ssh -i 키페어 ubuntu@인스턴스DNS
```

- nginx 설치
```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl status nginx
```

- 웹 브라우저에 접속 테스트
```bash
http://인스턴스DNS:80
```

## EC2에 Docker 사용하기

- ubuntu 설치
```bash
sudo apt update
sudo apt install -y docker.io
```

- 서비스 상태 확인
```bash
sudo systemctl status docker
```

- 부팅 시 자동 시작
```bash
sudo systemctl enable docker
```

- Docker 버젼 확인
```bash
sudo docker --version
```

## `sudo` 없이 docker 사용하기

- Docker 그룹에 현재 사용자 추가
```bash
sudo usermod -aG docker $USER
```

- 적용을 위해 로그아웃 후 다시 접속 또는 `newgrp docker` 명령어 사용하기

- `sudo` 없이 docker 확인
```bash
docker --version
```

## Docker Compose 사용하기

- 설치
```bash
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
-o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```

- 버젼 확인
```bash
docker compose version
```
