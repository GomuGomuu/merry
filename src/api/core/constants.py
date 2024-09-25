# IMPORT NAMED TUPLES
from collections import namedtuple

HTTP_METHODS = namedtuple("HTTP_METHODS", ["GET", "POST", "PUT", "DELETE"])(
    "GET",
    "POST",
    "PUT",
    "DELETE",
)
