## GGUF 변환 (llama.cpp 사용)

1. llama.cpp 설치
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
pip install -r requirements.txt
```

2. 모델 변환:
```bash
python convert_hf_to_gguf.py  <모델_폴더_경로> --outfile my_model.gguf --outtype f16
```

3. Ollama Modelfile 생성
```dockerfile
# 1. 변환된 GGUF 파일 경로
FROM ./model.gguf

# 2. 모델 매개변수 설정
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER stop "<|endoftext|>"

# 3. 템플릿 설정 (GPT-2 스타일)
TEMPLATE """
{{ .Prompt }}
"""

# 4. 시스템 메시지
SYSTEM "You are a helpful AI assistant trained on custom data."
```

4. Ollama 모델 등록 및 실행
모델 생성:
```bash
ollama create my-custom-gpt -f Modelfile
```

모델 실행:
```bash
ollama run my-custom-gpt
```
