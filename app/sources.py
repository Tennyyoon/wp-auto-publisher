import feedparser
from typing import List, Dict

def fetch_bizinfo_rss() -> List[Dict]:
    # 기업마당 RSS (운영 측 변경 가능. 안 되면 다음 단계에서 공식 API로 전환)
    url = "https://www.bizinfo.go.kr/uss/rss/bizinfoRss.do"
    feed = feedparser.parse(url)
    items = []
    for e in feed.entries[:30]:
        items.append({
            "id": e.get("id") or e.get("link"),
            "title": (e.get("title", "") or "").strip(),
            "summary": (e.get("summary", "") or "").strip(),
            "link": (e.get("link", "") or "").strip(),
            "category": "정부지원금 속보",
        })
    return items

PERFECT_GUIDE_POOL = [
    {
        "id": "gov24-subsidy24",
        "title": "보조금24로 내가 받을 수 있는 혜택 찾는 방법 정리",
        "summary": "정부24 보조금24에서 맞춤형 혜택을 조회하는 흐름과 준비사항을 정리합니다.",
        "link": "https://www.gov.kr/portal/rcvfvrSvc/dtlEx/138300000009",
        "category": "정부지원금 완벽정리",
    }
]

def fetch_perfect_guides() -> List[Dict]:
    return PERFECT_GUIDE_POOL.copy()
