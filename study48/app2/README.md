## uv 형식 jupyter 알아보기

- 프로젝트 생성

```bash
uv init .
```

- jupyter 모듈 설치

```bash
uv add --dev ipykernel
```

- jupyter 실행

```bash
uv run --with jupyter jupyter lab
```

## Docker 파일 복사

```bash
docker cp [파일경로및파일명] [컨테이너명]:[파일경로및파일명]
docker cp .\sample.txt master:/opt/spark/data/sample.txt
```
