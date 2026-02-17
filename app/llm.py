import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM = "너는 한국어 SEO 편집자다. 입력에 없는 정보는 추측하지 말고, 불확실하면 '확인 필요'로 남겨라."

def generate_post(category: str, item_title: str, item_summary: str, item_url: str) -> dict:
    prompt = f"""
[카테고리] {category}
[원문 제목] {item_title}
[원문 요약] {item_summary}
[원문 URL] {item_url}

요구사항:
- 1500~1800자(공백 포함) 한국어 글
- 제목(H1)에 핵심 키워드 1개를 그대로 포함
- 소제목(H2/H3) 구분 명확하게
- 본문에 핵심 키워드 2~3회 반복
- 마지막에 '출처' 섹션에 URL 포함
- 과장/단정 금지. 변경 가능성 1문장 포함.
- 출력은 JSON만:
{{
 "title": "...",
 "focus_keyword": "...",
 "excerpt": "...",
 "content_html": "...(h2/h3/p/ul 사용)",
 "image_query": "...(Pexels 검색어)",
 "image_alt": "..."
}}
"""
    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    text = resp.output_text
    return
