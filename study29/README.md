## Kafka 만들기
```yml
services:
  kafka:
    container_name: kafka
    image: apache/kafka:4.0.1
    ports:
      - 9092:9092
    networks:
      - my-bridge
    working_dir: /opt/kafka/bin/
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

networks:
  my-bridge:
    driver: bridge
```

```bash
docker network inspect study29_my-bridge   
```
- IP : `172.19.0.2` ***kafka IP***

## 1. App1 설정

```bash
uv init .
uv add fastapi --extra standard
uv add kafka-python
```

## UV 이미지 생성 `dockerfile`
```bash
FROM python:3.13.11

RUN apt-get update
RUN apt-get upgrade -y
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN pip install uv

WORKDIR /workspace

EXPOSE 8000
```

```bash
docker build -t uv:1 .
```

## App1 Container 생성

```bash
docker run -d -it -p 8001:8000 --network study29_my-bridge -v ./app1:/workspace --name app1 uv:1
```

- IP : `172.19.0.3` ***app1 IP***

## Docker Container 접속 하기

```bash
docker exec -it kafka /bin/bash
```

## Kafka 설치 위치
```bash
cd /opt/kafka/bin/
```

## 메시지 확인 
```bash
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test
```

## App2 Container 생성

```bash
docker run -d -it -p 8002:8000 --network study29_my-bridge -v ./app2:/workspace --name app2 uv:1
```

## App3 Container 생성
```bash
docker run -d -it -p 80:5173 --network study29_my-bridge -v ./app3:/workspace --name app3 node:24.13.0
```

## `vite.config.js` 설정
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath, URL } from 'url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/",
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: ['localhost'],
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    }
  },
})
```