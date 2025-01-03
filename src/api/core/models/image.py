import logging
import mimetypes
import uuid
from datetime import date

from django.core.files.base import ContentFile
from django.core.files.images import get_image_dimensions
from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail
from api.core.utils import slugify
import requests
from io import BytesIO

logger = logging.getLogger(__name__)


class AbstractImage(models.Model):
    class Meta:
        abstract = True

    src = ImageField(upload_to="img/", max_length=255)
    alt = models.CharField(max_length=255, blank=True, null=True)

    @property
    def dimensions(self):
        return get_image_dimensions(self.src)

    @property
    def height(self):
        return self.dimensions[1]

    @property
    def width(self):
        return self.dimensions[0]

    @property
    def ratio(self):
        x, y = self.dimensions
        return float(x) / float(y)

    @property
    def tag(self):
        return '<img img="%s" alt="%s" width="%d" height="%d"/>' % (
            self.src,
            self.alt,
            self.width,
            self.height,
        )

    def size(self, size):
        from PIL import ImageFile

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        try:
            return get_thumbnail(self.src, size, crop="center")
        except OSError:
            return None

    @property
    def micro(self):
        return self.size("60x60")

    @property
    def small(self):
        return self.size("86x78")

    @property
    def thumb(self):
        return self.size("250x250")

    def __str__(self):
        return self.src.url

    def url(self):
        return self.src.url

    def set_image(self, image, file_name=None, save=True):
        image_data = image.read()

        if hasattr(image, "name"):
            image_extension = image.name.split(".")[-1].split("?")[0]
        else:
            image_extension = "jpg"

        file_name = (
            f"{date.today()}-{uuid.uuid4()}-{slugify(file_name)}.{image_extension}"
            if file_name
            else f"{date.today()}-{uuid.uuid4()}-unnamed.{image_extension}"
        )

        src = ContentFile(image_data)
        self.src.save(file_name, src, save=save)

    def set_image_from_url(self, url, save=True):
        logger.debug(f"Downloading image from {url}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type")
            if not content_type or "image" not in content_type:
                raise ValueError(f"URL does not point to an image: {url}")

            image_content = BytesIO(response.content)
            image_name = url.split("/")[-1]

            image_extension = mimetypes.guess_extension(content_type.split(";")[0])

            if not image_extension:
                image_extension = (
                    image_name.split(".")[-1] if "." in image_name else "jpg"
                )

            image = ContentFile(image_content.read(), name=image_name)
            self.set_image(image, file_name=image_name, save=save)
            logger.debug(f"Image downloaded and set from {url}")

        except Exception as e:
            logger.error(f"Error downloading image from {url}: {e}")
            raise e
