import base64
import requests
from typing import Optional, Dict, Any

def _auth_header(user: str, app_password: str) -> Dict[str, str]:
    token = base64.b64encode(f"{user}:{app_password}".encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {token}"}

def wp_get_categories(base_url: str, user: str, app_password: str) -> Dict[str, int]:
    url = f"{base_url}/wp-json/wp/v2/categories?per_page=100"
    r = requests.get(url, headers=_auth_header(user, app_password), timeout=30)
    r.raise_for_status()
    cats = r.json()
    return {c["name"]: c["id"] for c in cats}

def wp_upload_image(
    base_url: str,
    user: str,
    app_password: str,
    image_bytes: bytes,
    filename: str,
    alt_text: str
) -> int:
    url = f"{base_url}/wp-json/wp/v2/media"
    headers = _auth_header(user, app_password)
    headers.update({
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    })

    r = requests.post(url, headers=headers, data=image_bytes, timeout=60)
    r.raise_for_status()
    media = r.json()
    media_id = media["id"]

    # alt text 설정
    patch_url = f"{base_url}/wp-json/wp/v2/media/{media_id}"
    r2 = requests.post(
        patch_url,
        headers=_auth_header(user, app_password),
        json={"alt_text": alt_text},
        timeout=30
    )
    r2.raise_for_status()

    return media_id

def wp_create_scheduled_post(
    base_url: str,
    user: str,
    app_password: str,
    title: str,
    content_html: str,
    excerpt: str,
    category_id: int,
    tags: Optional[list] = None,
    featured_media: Optional[int] = None,
    date_gmt_iso: Optional[str] = None,
) -> Dict[str, Any]:
    url = f"{base_url}/wp-json/wp/v2/posts"
    payload = {
        "title": title,
        "content": content_html,
        "excerpt": excerpt,
        "status": "future",
        "categories": [category_id],
    }
    if tags:
        payload["tags"] = tags
    if featured_media:
        payload["featured_media"] = featured_media
    if date_gmt_iso:
        payload["date_gmt"] = date_gmt_iso  # UTC 기준 예약시간

    r = requests.post(url, headers=_auth_header(user, app_password), json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
