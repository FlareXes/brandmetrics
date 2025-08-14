import re
from django.db.models import Sum
from .models import Payout
from datetime import datetime, timedelta
from django.utils import timezone

DATE_RANGE_RE = re.compile(
    r"(?:from|between)\s*(\d{4}-\d{2}-\d{2})\s*(?:to|and)\s*(\d{4}-\d{2}-\d{2})",
    re.IGNORECASE,
)


def parse_intent(text: str):
    t = text.strip().lower()
    # Payroll intents
    if "this week" in t:
        return ("payroll_range", "this_week")
    if "this month" in t:
        return ("payroll_range", "this_month")
    if "this year" in t:
        return ("payroll_range", "this_year")
    if "last month" in t:
        return ("payroll_range", "last_month")
    m = DATE_RANGE_RE.search(t)
    if m:
        return ("payroll_custom", (m.group(1), m.group(2)))

    # Customer orders/projects
    # e.g., "customer alice johnson" or "orders for alice"
    cust = None
    if t.startswith("customer "):
        cust = text.strip()[9:].strip()
    else:
        m = re.search(r"(?:customer|orders? for)\s+(.+)", t, re.IGNORECASE)
        if m:
            cust = m.group(1).strip()
    if cust:
        return ("orders_by_customer", cust)

    return ("unknown", None)


def start_of_week_ist(dt):
    # Monday as start of week
    d = dt.date()
    return d - timedelta(days=d.weekday())


def month_bounds(dt):
    first = dt.replace(day=1).date()
    if dt.month == 12:
        next_first = dt.replace(year=dt.year+1, month=1, day=1).date()
    else:
        next_first = dt.replace(month=dt.month+1, day=1).date()
    last = next_first - timedelta(days=1)
    return first, last


def prev_month_bounds(dt):
    if dt.month == 1:
        prev = dt.replace(year=dt.year-1, month=12, day=1)
    else:
        prev = dt.replace(month=dt.month-1, day=1)
    first = prev.date()
    # end of prev month = first of this month - 1 day
    this_first = dt.replace(day=1).date()
    last = this_first - timedelta(days=1)
    return first, last


def payroll_sum(start_date, end_date):
    q = Payout.objects.filter(
        paying_date__gte=start_date, paying_date__lte=end_date)
    total = q.aggregate(total=Sum("amount"))["total"] or 0
    return float(total)


def ist_now():
    user_timezone = timezone.get_fixed_timezone(5 * 60)
    naive_datetime = datetime.now()
    return timezone.make_aware(naive_datetime, user_timezone)
