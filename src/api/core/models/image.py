import uuid
from datetime import date

from django.core.files.base import ContentFile
from django.core.files.images import get_image_dimensions
from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail

from api.core.utils import slugify


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
        file_name = (
            f"{date.today()}-{uuid.uuid4()}-{slugify(file_name)}.{image.content_type.split('/')[-1]}"
            if file_name
            else f"{date.today()}-{uuid.uuid4()}-unnamed.{image.content_type.split('/')[-1]}"
        )
        src = ContentFile(image_data)
        self.src.save(file_name, src, save=save)
