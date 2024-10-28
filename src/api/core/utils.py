from datetime import datetime, timedelta
import logging
import unicodedata
import os

logger = logging.getLogger(__name__)


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


def save_image_to_disk(image, path):
    logger.info(f"Saving image to disk: {path}")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(image.read())
        logger.info("Image saved")
        return path
    except Exception as e:
        logger.error(f"Error saving image to disk: {e}")
        return None


def delete_image_from_disk(path):
    try:
        logger.info(f"Deleting image from disk: {path}")
        os.remove(path)
        logger.info("Image deleted")
        return True
    except Exception as e:
        logger.error(f"Error deleting image from disk: {e}")
        return False
