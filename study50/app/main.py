import ollama

# ---------------------------
# Ollama LLM 호출 함수
# ---------------------------
def llm_call_structured(prompt: str, model: str = "gemma3:4b"):

  # Ollama에 LLM 요청
  response = ollama.chat(
    model=model,
    messages=[{"role": "user", "content": prompt}]
  )

  # 모델 응답 텍스트 추출
  text = response["message"]["content"]

  # JSON 파싱 시도
  try:
    print(text)
  except Exception as e:
    print(f"응답 오류: {e}")

# ------------------------------------------------------
# 메인 실행 함수
# ------------------------------------------------------
def main():
  try:
    # 프롬프트 설정
    prompt = """
      안녕하세요
    """

    # LLM 호출
    llm_call_structured(prompt)
  except Exception as e:
    print(f"오류 발생: {e}")
    return 1
  return 0

# ------------------------------------------------------
# 프로그램 실행
# ------------------------------------------------------
if __name__ == "__main__":
  exit(main())
