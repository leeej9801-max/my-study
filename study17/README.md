## UV 프로젝트 초기화
```bash
uv init .
```

## FastAPI 모듈 추가
```bash
uv add fastapi --extra standard
```

## FastAPI 기본 설정 `main.py`
```python
from fastapi import FastAPI
app = FastAPI()
```

## FastAPI 개발자 모드 실행
```bash
uv run fastapi dev
```

## FastAPI 서비스 모드 실행
```bash
uv run fastapi run
```
