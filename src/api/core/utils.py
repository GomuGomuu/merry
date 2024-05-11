import unicodedata


def slugify(name):
    normalized = unicodedata.normalize("NFKD", name)
    slug = "".join([c for c in normalized if not unicodedata.combining(c)])
    slug = slug.lower().strip()
    slug = "".join([c if c.isalnum() or c == "-" else " " for c in slug])
    slug = "-".join(slug.split())
    return slug
