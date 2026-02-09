## docker build 캐시 삭제
```bash
docker builder prune -f
```

## docker container 만들기
```bash
docker compose up -d
```

## redis 확인
```
docker exec -it redis redis-cli

keys *
```

## kafka 확인
```bash
docker exec -it kafka /bin/bash

./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test
```
