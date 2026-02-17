# app/main.py
import os
import random
from app.utils import now_kst, schedule_times_kst_for_today, kst_to_utc
from app.state import load_published_ids, save_published_ids
from app.sources import fetch_bizinfo_rss, fetch_perfect_guides
from app.llm import generate_post
from app.images import fetch_pexels_image
from app.wp import wp_get_categories, wp_upload_image, wp_create_scheduled_post

CATEGORIES = ["공공기관채용", "대사관채용정보", "병원채용정보", "정부지원금 속보", "정부지원금 완벽정리"]

def pick_items(published: set):
    candidates = []
    candidates += fetch_bizinfo_rss()
    candidates += fetch_perfect_guides()

    by_cat = {}
    for it in candidates:
        by_cat.setdefault(it["category"], []).append(it)

    available = [c for c in CATEGORIES if c in by_cat]
    chosen = random.sample(available, k=min(3, len(available)))
    random.shuffle(chosen)

    picked = []
    for c in chosen:
        pool = [x for x in by_cat[c] if x["id"] not in published]
        if pool:
            picked.append(pool[0])
    return picked

def main():
    wp_base = os.environ["WP_BASE_URL"].rstrip("/")
    wp_user = os.environ["WP_USERNAME"]
    wp_pass = os.environ["WP_APP_PASSWORD"]
    pexels_key = os.environ["PEXELS_API_KEY"]

    published = load_published_ids()
    cats = wp_get_categories(wp_base, wp_user, wp_pass)

    base = now_kst()
    times_kst = schedule_times_kst_for_today(base)  # 08/13/18 KST
    items = pick_items(published)

    for i, it in enumerate(items[:3]):
        post = generate_post(it["category"], it["title"], it["summary"], it["link"])

        img_bytes, photographer = fetch_pexels_image(pexels_key, post["image_query"])
        media_id = wp_upload_image(wp_base, wp_user, wp_pass, img_bytes, "cover.jpg", post["image_alt"])

        dt_utc = kst_to_utc(times_kst[i]).replace(microsecond=0)
        date_gmt = dt_utc.isoformat().replace("+00:00", "Z")

        content_html = post["content_html"] + f'<p><small>Image: Photo by {photographer} on Pexels</small></p>'

        category_id = cats.get(it["category"])
        if not category_id:
            raise RuntimeError(f"WP category not found: {it['category']}")

        wp_create_scheduled_post(
            wp_base, wp_user, wp_pass,
            title=post["title"],
            content_html=content_html,
            excerpt=post["excerpt"],
            category_id=category_id,
            featured_media=media_id,
            date_gmt_iso=date_gmt,
        )

        published.add(it["id"])

    save_published_ids(published)

if __name__ == "__main__":
    main()
