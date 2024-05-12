from datetime import datetime, timedelta

import unicodedata


def slugify(name):
    normalized = unicodedata.normalize("NFKD", name)
    slug = "".join([c for c in normalized if not unicodedata.combining(c)])
    slug = slug.lower().strip()
    slug = "".join([c if c.isalnum() or c == "-" else " " for c in slug])
    slug = "-".join(slug.split())
    return slug


def get_days_range(date_from=None, date_to=None, default_days=15):
    """
    return: date_from, date_to
    """
    if date_to and not date_from:
        date_from = datetime.strptime(date_to, "%Y-%m-%d").date() - timedelta(
            days=default_days
        )
    elif date_from and not date_to:
        date_to = datetime.strptime(date_from, "%Y-%m-%d").date() + timedelta(
            days=default_days
        )
    else:
        date_to = datetime.now().date()
        date_from = date_to - timedelta(days=15)

    return date_from, date_to
