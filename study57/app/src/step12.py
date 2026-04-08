from __future__ import annotations

import json
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Literal
from typing_extensions import TypedDict

import psycopg
from psycopg.rows import dict_row
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

# ============================================================
# step14 v1.1 - DB 연결 버전
# 목적:
#   ESG 미디어/보고서/자사 문서를 받아
#   ESG Signal Annotation 데이터를 생성하고 PostgreSQL에 저장한다.
# 범위:
#   - issue / sentiment / signal_type / severity / reason_span 추출
#   - confidence 계산
#   - auto / review queue 분기
#   - DB insert 자동화
# 제외:
#   - metric 매핑
#   - materiality score 계산
#   - retry loop
# ============================================================

# -------------------------
# 0) 설정
# -------------------------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "esg_platform",
    "user": "postgres",
    "password": "esg1234",
}

OLLAMA_MODEL = "llama3.2:3b"
REVIEW_THRESHOLD = 0.70
MAX_PARAGRAPHS = 5

# TODO:
ISSUE_POOL = [
    "Climate", "Energy", "Water", "Pollution", "Biodiversity",
    "Product_env", "Circularity", "Labor", "Safety", "Talent", "Diversity",
    "Human Rights", "Supply Chain_env", "Community", "Product_resp",
    "Privacy", "Governance", "Risk", "Ethics", "Business Conduct",
    "Data Governance", "Compliance", "Sustainable investment", "Supply Chain_social", 
]

SIGNAL_TYPES = ["regulation", "incident", "litigation", "disclosure", "investment", "performance"]
SEVERITY_LEVELS = ["low", "medium", "high"]
SENTIMENT_LABELS = ["positive", "neutral", "negative"]

# -------------------------
# 1) TypedDict
# -------------------------
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
    signal_type: Literal["regulation", "incident", "litigation", "disclosure", "investment", "performance"]
    severity_level: Literal["low", "medium", "high"]
    reason_span: str
    confidence_score: float
    label_source: Literal["rule", "model", "human", "reviewed"]
    review_status: Literal["raw", "auto_labeled", "needs_review", "reviewed"]
    review_note: str


class SignalState(TypedDict, total=False):
    source_url: str
    source_type: str
    source_name: str
    title: str
    published_at: str
    raw_text: str

    article: ArticleRecord
    text_units: List[TextUnitRecord]
    annotations: List[AnnotationRecord]
    auto_saved: List[AnnotationRecord]
    review_queue: List[AnnotationRecord]
    debug_logs: List[str]
    error: str


# -------------------------
# 2) DB 유틸
# -------------------------
def get_conn():
    return psycopg.connect(**DB_CONFIG, row_factory=dict_row)


def init_db() -> None:
    ddl = """
    CREATE TABLE IF NOT EXISTS issue_pool (
        issue_code TEXT PRIMARY KEY,
        issue_name_ko TEXT,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS signal_article (
        article_id UUID PRIMARY KEY,
        source_type TEXT NOT NULL,
        source_name TEXT NOT NULL,
        source_url TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        published_at TIMESTAMPTZ NULL,
        crawled_at TIMESTAMPTZ NOT NULL,
        raw_text TEXT,
        language TEXT DEFAULT 'ko',
        country TEXT DEFAULT 'KR',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

    CREATE INDEX IF NOT EXISTS idx_signal_article_published_at
    ON signal_article (published_at DESC);

    CREATE TABLE IF NOT EXISTS signal_text_unit (
        text_unit_id UUID PRIMARY KEY,
        article_id UUID NOT NULL REFERENCES signal_article(article_id) ON DELETE CASCADE,
        unit_type TEXT NOT NULL,
        unit_order INTEGER NOT NULL,
        text_unit TEXT NOT NULL,
        is_core_signal BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        UNIQUE (article_id, unit_type, unit_order)
    );

    CREATE INDEX IF NOT EXISTS idx_signal_text_unit_article
    ON signal_text_unit (article_id);

    CREATE TABLE IF NOT EXISTS signal_annotation (
        annotation_id UUID PRIMARY KEY,
        text_unit_id UUID NOT NULL UNIQUE REFERENCES signal_text_unit(text_unit_id) ON DELETE CASCADE,
        primary_issue TEXT NOT NULL REFERENCES issue_pool(issue_code),
        secondary_issues JSONB NOT NULL DEFAULT '[]'::jsonb,
        sentiment_label TEXT NOT NULL,
        signal_type TEXT NOT NULL,
        severity_level TEXT NOT NULL,
        reason_span TEXT,
        confidence_score NUMERIC(4,2),
        label_source TEXT NOT NULL DEFAULT 'model',
        review_status TEXT NOT NULL DEFAULT 'raw',
        review_note TEXT,
        model_name TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

    CREATE INDEX IF NOT EXISTS idx_signal_annotation_primary_issue
    ON signal_annotation (primary_issue);

    CREATE INDEX IF NOT EXISTS idx_signal_annotation_review_status
    ON signal_annotation (review_status);
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(ddl)
            for issue in ISSUE_POOL:
                cur.execute(
                    """
                    INSERT INTO issue_pool (issue_code, issue_name_ko)
                    VALUES (%s, %s)
                    ON CONFLICT (issue_code) DO NOTHING
                    """,
                    (issue, issue),
                )
        conn.commit()


def save_article(conn: psycopg.Connection, article: ArticleRecord) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO signal_article (
                article_id, source_type, source_name, source_url, title,
                published_at, crawled_at, raw_text, language, country
            ) VALUES (
                %(article_id)s::uuid, %(source_type)s, %(source_name)s, %(source_url)s, %(title)s,
                NULLIF(%(published_at)s, '')::timestamptz,
                %(crawled_at)s::timestamptz,
                %(raw_text)s, %(language)s, %(country)s
            )
            ON CONFLICT (source_url) DO UPDATE SET
                title = EXCLUDED.title,
                raw_text = EXCLUDED.raw_text,
                published_at = EXCLUDED.published_at
            """,
            article,
        )


def save_text_units(conn: psycopg.Connection, text_units: List[TextUnitRecord]) -> None:
    with conn.cursor() as cur:
        for unit in text_units:
            cur.execute(
                """
                INSERT INTO signal_text_unit (
                    text_unit_id, article_id, unit_type, unit_order, text_unit, is_core_signal
                ) VALUES (
                    %(text_unit_id)s::uuid, %(article_id)s::uuid, %(unit_type)s,
                    %(unit_order)s, %(text_unit)s, %(is_core_signal)s
                )
                ON CONFLICT (article_id, unit_type, unit_order) DO UPDATE SET
                    text_unit = EXCLUDED.text_unit,
                    is_core_signal = EXCLUDED.is_core_signal
                """,
                unit,
            )


def save_annotations(conn: psycopg.Connection, anns: List[AnnotationRecord], review_status: str) -> None:
    with conn.cursor() as cur:
        for ann in anns:
            cur.execute(
                """
                INSERT INTO signal_annotation (
                    annotation_id, text_unit_id, primary_issue, secondary_issues,
                    sentiment_label, signal_type, severity_level, reason_span,
                    confidence_score, label_source, review_status, review_note, model_name
                ) VALUES (
                    gen_random_uuid(),
                    %(text_unit_id)s::uuid,
                    %(primary_issue)s,
                    %(secondary_issues)s::jsonb,
                    %(sentiment_label)s,
                    %(signal_type)s,
                    %(severity_level)s,
                    %(reason_span)s,
                    %(confidence_score)s,
                    %(label_source)s,
                    %(review_status)s,
                    %(review_note)s,
                    %(model_name)s
                )
                ON CONFLICT (text_unit_id) DO UPDATE SET
                    primary_issue = EXCLUDED.primary_issue,
                    secondary_issues = EXCLUDED.secondary_issues,
                    sentiment_label = EXCLUDED.sentiment_label,
                    signal_type = EXCLUDED.signal_type,
                    severity_level = EXCLUDED.severity_level,
                    reason_span = EXCLUDED.reason_span,
                    confidence_score = EXCLUDED.confidence_score,
                    label_source = EXCLUDED.label_source,
                    review_status = EXCLUDED.review_status,
                    review_note = EXCLUDED.review_note,
                    model_name = EXCLUDED.model_name,
                    updated_at = NOW()
                """,
                {
                    **ann,
                    "secondary_issues": json.dumps(ann.get("secondary_issues", []), ensure_ascii=False),
                    "review_status": review_status,
                    "model_name": OLLAMA_MODEL,
                },
            )


# -------------------------
# 3) Prompt / LLM
# -------------------------
llm = ChatOllama(model=OLLAMA_MODEL, temperature=0)

PROMPT = PromptTemplate.from_template(
    """
다음 텍스트를 ESG 기준으로 분석하라.

[이슈 목록]
{issue_pool}

[텍스트]
{text}

JSON으로만 출력:
{{
  "primary_issue":"",
  "secondary_issues":[],
  "sentiment_label":"",
  "signal_type":"",
  "severity_level":"",
  "reason_span":""
}}
"""
)

chain = PROMPT | llm
JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def parse_json(x: Any) -> Dict[str, Any]:
    text = x.content if hasattr(x, "content") else str(x)
    match = JSON_RE.search(text)
    if not match:
        raise ValueError(f"JSON 파싱 실패: {text}")
    return json.loads(match.group(0))


# -------------------------
# 4) 유틸
# -------------------------
def new_uuid() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def confidence(ann: Dict[str, Any], text: str) -> float:
    score = 0.0
    if ann.get("primary_issue") in ISSUE_POOL:
        score += 0.30
    if ann.get("sentiment_label") in SENTIMENT_LABELS:
        score += 0.10
    if ann.get("signal_type") in SIGNAL_TYPES:
        score += 0.10
    if ann.get("severity_level") in SEVERITY_LEVELS:
        score += 0.10
    if ann.get("reason_span"):
        score += 0.10
    if ann.get("reason_span") and ann["reason_span"] in text:
        score += 0.30
    return round(score, 2)


# -------------------------
# 5) Node
# -------------------------
def init_article(state: SignalState) -> SignalState:
    article: ArticleRecord = {
        "article_id": new_uuid(),
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
        "debug_logs": state.get("debug_logs", []) + [f"init_article: {article['article_id']}"]
    }


def split_text(state: SignalState) -> SignalState:
    article = state["article"]
    raw_text = article.get("raw_text", "")
    title = article.get("title", "")

    text_units: List[TextUnitRecord] = []
    order = 1

    if title:
        text_units.append({
            "text_unit_id": new_uuid(),
            "article_id": article["article_id"],
            "unit_type": "title",
            "unit_order": order,
            "text_unit": title,
            "is_core_signal": True,
        })
        order += 1

    parts = [p.strip() for p in raw_text.split("\n") if p.strip()]
    for p in parts[:MAX_PARAGRAPHS]:
        text_units.append({
            "text_unit_id": new_uuid(),
            "article_id": article["article_id"],
            "unit_type": "paragraph",
            "unit_order": order,
            "text_unit": p,
            "is_core_signal": True,
        })
        order += 1

    return {
        "text_units": text_units,
        "debug_logs": state.get("debug_logs", []) + [f"split_text: {len(text_units)} units"]
    }


def classify(state: SignalState) -> SignalState:
    anns: List[AnnotationRecord] = []

    for unit in state["text_units"]:
        res = parse_json(chain.invoke({
            "issue_pool": ", ".join(ISSUE_POOL),
            "text": unit["text_unit"],
        }))

        ann: AnnotationRecord = {
            "text_unit_id": unit["text_unit_id"],
            "primary_issue": res.get("primary_issue", ""),
            "secondary_issues": (res.get("secondary_issues", []) or [])[:2],
            "sentiment_label": res.get("sentiment_label", ""),
            "signal_type": res.get("signal_type", ""),
            "severity_level": res.get("severity_level", ""),
            "reason_span": res.get("reason_span", ""),
            "confidence_score": confidence(res, unit["text_unit"]),
            "label_source": "model",
            "review_status": "raw",
            "review_note": "",
        }
        anns.append(ann)

    return {
        "annotations": anns,
        "debug_logs": state.get("debug_logs", []) + ["classify: done"]
    }


def route(state: SignalState) -> SignalState:
    auto_saved: List[AnnotationRecord] = []
    review_queue: List[AnnotationRecord] = []

    for a in state["annotations"]:
        if a["confidence_score"] < REVIEW_THRESHOLD:
            a["review_status"] = "needs_review"
            a["review_note"] = "confidence 낮음 또는 reason 검증 미흡"
            review_queue.append(a)
        else:
            a["review_status"] = "auto_labeled"
            auto_saved.append(a)

    return {
        "auto_saved": auto_saved,
        "review_queue": review_queue,
        "debug_logs": state.get("debug_logs", []) + [
            f"route: auto={len(auto_saved)}, review={len(review_queue)}"
        ]
    }


def save_auto(state: SignalState) -> SignalState:
    with get_conn() as conn:
        save_article(conn, state["article"])
        save_text_units(conn, state["text_units"])
        save_annotations(conn, state.get("auto_saved", []), review_status="auto_labeled")
        conn.commit()
    return {
        "debug_logs": state.get("debug_logs", []) + ["save_auto: committed"]
    }


def save_review(state: SignalState) -> SignalState:
    with get_conn() as conn:
        save_article(conn, state["article"])
        save_text_units(conn, state["text_units"])
        save_annotations(conn, state.get("review_queue", []), review_status="needs_review")
        conn.commit()
    return {
        "debug_logs": state.get("debug_logs", []) + ["save_review: committed"]
    }


def router(state: SignalState) -> Literal["save_review", "save_auto"]:
    return "save_review" if state.get("review_queue") else "save_auto"


# -------------------------
# 6) Graph
# -------------------------
def build() -> Any:
    g = StateGraph(SignalState)
    g.add_node("init_article", init_article)
    g.add_node("split", split_text)
    g.add_node("classify", classify)
    g.add_node("route", route)
    g.add_node("save_auto", save_auto)
    g.add_node("save_review", save_review)

    g.add_edge(START, "init_article")
    g.add_edge("init_article", "split")
    g.add_edge("split", "classify")
    g.add_edge("classify", "route")
    g.add_conditional_edges("route", router)
    g.add_edge("save_auto", END)
    g.add_edge("save_review", END)
    return g.compile()


if __name__ == "__main__":
    init_db()
    engine = build()

    result = engine.invoke(
        {
            "source_url": "https://www.impacton.net/news/articleView.html?idxno=18412",
            "source_type": "news",
            "source_name": "IMPACT ON",
            "title": "정부, 배출량 산정 역량 강화 추진…CBAM 대응 데이터 기반 구축",
            "published_at": "2026-04-01",
            "raw_text": "정부는 EU 탄소국경조정제도와 ESG 공시 의무 강화에 대응해 기업의 온실가스 배출량 산정 역량 강화 정책을 추진하고 있다. 전력 배출계수 고도화와 전 과정목록 데이터베이스 구축이 포함됐다.\n해당 데이터는 올해 하반기부터 매년 업데이트될 예정이다. 3월 26일 정책토론회를 통해 제도 보완과 기업 지원 방향 논의가 진행된다.",
        }
    )

    print(json.dumps(result.get("debug_logs", []), ensure_ascii=False, indent=2))
