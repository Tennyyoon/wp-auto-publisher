import requests
from typing import Tuple

def fetch_pexels_image(pexels_key: str, query: str) -> Tuple[bytes, str]:
    # 검색
    r = requests.get(
        "https://api.pexels.com/v1/search",
        headers={"Authorization": pexels_key},
        params={"query": query, "per_page": 1, "orientation": "landscape"},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if not data.get("photos"):
        raise RuntimeError("No image results from Pexels.")

    photo = data["photos"][0]
    img_url = photo["src"]["large"]
    photographer = photo.get("photographer", "Pexels")

    # 다운로드
    img = requests.get(img_url, timeout=60)
    img.raise_for_status()
    return img.content, photographer
