from datetime import datetime, timezone
from dateutil import tz

KST = tz.gettz("Asia/Seoul")

def now_kst() -> datetime:
    return datetime.now(tz=KST)

def kst_to_utc(dt_kst: datetime) -> datetime:
    return dt_kst.astimezone(timezone.utc)

def schedule_times_kst_for_today(base_kst: datetime):
    """Return 3 datetime objects in KST: today 08:00, 13:00, 18:00."""
    d = base_kst.astimezone(KST).date()
    t1 = datetime(d.year, d.month, d.day, 8, 0, 0, tzinfo=KST)
    t2 = datetime(d.year, d.month, d.day, 13, 0, 0, tzinfo=KST)
    t3 = datetime(d.year, d.month, d.day, 18, 0, 0, tzinfo=KST)
    return [t1, t2, t3]
