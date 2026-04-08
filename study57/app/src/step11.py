from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from typing_extensions import TypedDict
from dataclasses import dataclass
import json
import re
import uuid
from datetime import datetime

from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama


# =========================
# 1) 고정 기준: Issue Pool
# =========================
# 주의:
# - 이 값은 임시 예시다.
# - 실제 운영에서는 반드시 Master -> Issue 매핑표를 기준으로 교체해야 한다.
ISSUE_POOL: List[str] = [
    "Climate",
    "Energy",
    "Water",
    "Pollution",
    "Waste",
    "Biodiversity",
    "Product",
    "Circularity",
    "Labor",
    "Safety",
    "Talent",
    "Diversity",
    "Human Rights",
    "Supply Chain",
    "Community",
    "Product Liability",
    "Privacy",
    "Governance",
    "Risk",
    "Ethics",
    "Business Conduct",
    "Data Governance",
    "Compliance",
]

SIGNAL_TYPES = [
    "regulation",
    "incident",
    "litigation",
    "disclosure",
    "investment",
    "performance",
]

SEVERITY_LEVELS = ["low", "medium", "high"]
SENTIMENT_LABELS = ["positive", "neutral", "negative"]


# =========================
# 2) 저장용 표준 스키마
# =========================
class ArticleRecord(TypedDict, total=False):
    article_id: str
    source_type: str
    source_name: str
    source_url: str
    title: str
    published_at: str
    crawled_at: str
    raw_text: str
    language: str
    country: str


class TextUnitRecord(TypedDict, total=False):
    text_unit_id: str
    article_id: str
    unit_type: Literal["title", "lead", "paragraph", "sentence"]
    unit_order: int
    text_unit: str
    is_core_signal: bool


class AnnotationRecord(TypedDict, total=False):
    text_unit_id: str
    primary_issue: str
    secondary_issues: List[str]
    sentiment_label: Literal["positive", "neutral", "negative"]
    signal_type: Literal[
        "regulation", "incident", "litigation", "disclosure", "investment", "performance"
    ]
    severity_level: Literal["low", "medium", "high"]
    label_source: Literal["rule", "model", "reviewed"]
    review_status: Literal["raw", "auto_labeled", "reviewed"]
    review_note: str


class SignalState(TypedDict, total=False):
    # 입력
    source_url: str
    source_type: str
    source_name: str
    title: str
    published_at: str
    raw_text: str

    # 중간 결과
    article: ArticleRecord
    text_units: List[TextUnitRecord]
    annotations: List[AnnotationRecord]

    # 운영용
    error: str
    debug_logs: List[str]


# =========================
# 3) LLM + PromptTemplate
# =========================
# 실제 운영에서는 temperature=0 유지 권장
llm = ChatOllama(model="llama3.2:3b", temperature=0)

ISSUE_PROMPT = PromptTemplate.from_template(
    """
당신은 ESG 미디어 분석용 issue 분류기다.

[목표]
아래 텍스트를 읽고 issue pool 기준으로 분류하라.

[규칙]
1. 반드시 primary_issue 1개를 선택
2. secondary_issues는 최대 2개까지 선택
3. issue는 반드시 아래 목록에서만 선택
4. 결과는 JSON만 출력

[issue pool]
{issue_pool}

[텍스트]
{text_unit}

반드시 아래 형식으로만 답하라:
{{
  "primary_issue": "...",
  "secondary_issues": ["...", "..."]
}}
""".strip()
)

SENTIMENT_PROMPT = PromptTemplate.from_template(
    """
당신은 ESG 뉴스 감성 분류기다.

[기준]
- positive: 개선, 투자 확대, 성과 달성, 정책 강화
- neutral: 단순 공시, 발표, 일반 동향, 중립적 설명
- negative: 사고, 유출, 위반, 제재, 소송, 벌금, 리스크 확대

[텍스트]
{text_unit}

반드시 아래 JSON 형식으로만 답하라:
{{
  "sentiment_label": "positive|neutral|negative"
}}
""".strip()
)

SIGNAL_TYPE_PROMPT = PromptTemplate.from_template(
    """
당신은 ESG signal_type 분류기다.

[선택지]
- regulation
- incident
- litigation
- disclosure
- investment
- performance

[텍스트]
{text_unit}

반드시 아래 JSON 형식으로만 답하라:
{{
  "signal_type": "..."
}}
""".strip()
)

SEVERITY_PROMPT = PromptTemplate.from_template(
    """
당신은 ESG signal severity 판정기다.

[기준]
- low: 일반 동향, 경미한 언급
- medium: 중요도 있으나 대형 사건은 아님
- high: 대규모 사고, 유출, 제재, 중대한 규제 영향

[텍스트]
{text_unit}

반드시 아래 JSON 형식으로만 답하라:
{{
  "severity_level": "low|medium|high"
}}
""".strip()
)

issue_chain = ISSUE_PROMPT | llm
sentiment_chain = SENTIMENT_PROMPT | llm
signal_type_chain = SIGNAL_TYPE_PROMPT | llm
severity_chain = SEVERITY_PROMPT | llm


# =========================
# 4) 유틸
# =========================
def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


def parse_json_from_llm(raw: str) -> Dict[str, Any]:
    match = JSON_BLOCK_RE.search(raw)
    if not match:
        raise ValueError(f"JSON 블록을 찾을 수 없습니다: {raw}")
    return json.loads(match.group(0))


# =========================
# 5) Node 구현
# =========================
def init_article(state: SignalState) -> SignalState:
    article: ArticleRecord = {
        "article_id": new_id("article"),
        "source_type": state.get("source_type", "news"),
        "source_name": state.get("source_name", "unknown"),
        "source_url": state.get("source_url", ""),
        "title": state.get("title", ""),
        "published_at": state.get("published_at", ""),
        "crawled_at": now_iso(),
        "raw_text": state.get("raw_text", ""),
        "language": "ko",
        "country": "KR",
    }
    return {
        "article": article,
        "debug_logs": [f"init_article: {article['article_id']}"]
    }


def split_text_units(state: SignalState) -> SignalState:
    article = state["article"]
    title = article.get("title", "").strip()
    raw_text = article.get("raw_text", "").strip()

    text_units: List[TextUnitRecord] = []
    order = 1

    if title:
        text_units.append({
            "text_unit_id": new_id("tu"),
            "article_id": article["article_id"],
            "unit_type": "title",
            "unit_order": order,
            "text_unit": title,
            "is_core_signal": True,
        })
        order += 1

    paragraphs = [p.strip() for p in raw_text.split("\n") if p.strip()]
    for p in paragraphs[:5]:  # 초기 운영은 최대 5개 문단까지만
        text_units.append({
            "text_unit_id": new_id("tu"),
            "article_id": article["article_id"],
            "unit_type": "paragraph",
            "unit_order": order,
            "text_unit": p,
            "is_core_signal": True,
        })
        order += 1

    return {
        "text_units": text_units,
        "debug_logs": state.get("debug_logs", []) + [f"split_text_units: {len(text_units)} units"]
    }


def classify_issue(state: SignalState) -> SignalState:
    annotations = state.get("annotations", [])
    for unit in state.get("text_units", []):
        raw = issue_chain.invoke({
            "issue_pool": ", ".join(ISSUE_POOL),
            "text_unit": unit["text_unit"],
        })
        content = raw.content if hasattr(raw, "content") else str(raw)
        parsed = parse_json_from_llm(content)

        annotations.append({
            "text_unit_id": unit["text_unit_id"],
            "primary_issue": parsed["primary_issue"],
            "secondary_issues": parsed.get("secondary_issues", []),
            "label_source": "model",
            "review_status": "auto_labeled",
            "review_note": "",
        })

    return {
        "annotations": annotations,
        "debug_logs": state.get("debug_logs", []) + ["classify_issue: done"]
    }


def classify_sentiment(state: SignalState) -> SignalState:
    unit_map = {u["text_unit_id"]: u for u in state.get("text_units", [])}
    annotations = state.get("annotations", [])

    for ann in annotations:
        raw = sentiment_chain.invoke({"text_unit": unit_map[ann["text_unit_id"]]["text_unit"]})
        content = raw.content if hasattr(raw, "content") else str(raw)
        parsed = parse_json_from_llm(content)
        ann["sentiment_label"] = parsed["sentiment_label"]

    return {
        "annotations": annotations,
        "debug_logs": state.get("debug_logs", []) + ["classify_sentiment: done"]
    }


def classify_signal_type(state: SignalState) -> SignalState:
    unit_map = {u["text_unit_id"]: u for u in state.get("text_units", [])}
    annotations = state.get("annotations", [])

    for ann in annotations:
        raw = signal_type_chain.invoke({"text_unit": unit_map[ann["text_unit_id"]]["text_unit"]})
        content = raw.content if hasattr(raw, "content") else str(raw)
        parsed = parse_json_from_llm(content)
        ann["signal_type"] = parsed["signal_type"]

    return {
        "annotations": annotations,
        "debug_logs": state.get("debug_logs", []) + ["classify_signal_type: done"]
    }


def classify_severity(state: SignalState) -> SignalState:
    unit_map = {u["text_unit_id"]: u for u in state.get("text_units", [])}
    annotations = state.get("annotations", [])

    for ann in annotations:
        raw = severity_chain.invoke({"text_unit": unit_map[ann["text_unit_id"]]["text_unit"]})
        content = raw.content if hasattr(raw, "content") else str(raw)
        parsed = parse_json_from_llm(content)
        ann["severity_level"] = parsed["severity_level"]

    return {
        "annotations": annotations,
        "debug_logs": state.get("debug_logs", []) + ["classify_severity: done"]
    }


def save_results(state: SignalState) -> SignalState:
    # TODO: 실제 저장소(PostgreSQL / CSV / Google Sheet / S3) 연결
    print("\n=== ARTICLE ===")
    print(json.dumps(state.get("article", {}), ensure_ascii=False, indent=2))

    print("\n=== TEXT UNITS ===")
    print(json.dumps(state.get("text_units", []), ensure_ascii=False, indent=2))

    print("\n=== ANNOTATIONS ===")
    print(json.dumps(state.get("annotations", []), ensure_ascii=False, indent=2))

    return {
        "debug_logs": state.get("debug_logs", []) + ["save_results: printed"]
    }


def build_signal_graph():
    builder = StateGraph(SignalState)
    builder.add_node("init_article", init_article)
    builder.add_node("split_text_units", split_text_units)
    builder.add_node("classify_issue", classify_issue)
    builder.add_node("classify_sentiment", classify_sentiment)
    builder.add_node("classify_signal_type", classify_signal_type)
    builder.add_node("classify_severity", classify_severity)
    builder.add_node("save_results", save_results)

    builder.add_edge(START, "init_article")
    builder.add_edge("init_article", "split_text_units")
    builder.add_edge("split_text_units", "classify_issue")
    builder.add_edge("classify_issue", "classify_sentiment")
    builder.add_edge("classify_sentiment", "classify_signal_type")
    builder.add_edge("classify_signal_type", "classify_severity")
    builder.add_edge("classify_severity", "save_results")
    builder.add_edge("save_results", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_signal_graph()
    state: SignalState = {
        "source_url": "https://example.com/article/1",
        "source_type": "news",
        "source_name": "IMPACT ON",
        "title": "KT·롯데카드 해킹 사고로 ESG 평가 큰 폭으로 감점",
        "published_at": "2026-04-08",
        "raw_text": "ESG 평가기관 서스틴베스트가 KT와 롯데카드에서 연이어 발생한 해킹 피해와 관련해 정보보호 리스크의 심각성이 크다고 밝혔다.\nKT는 고객 개인정보 노출 피해 금액과 피해 고객 규모를 발표했다.\n롯데카드는 해킹으로 유출된 정보가 200GB에 달한다고 밝혔다.",
    }
    result = graph.invoke(state)
    print("\n=== DEBUG LOGS ===")
    print(result.get("debug_logs", []))
