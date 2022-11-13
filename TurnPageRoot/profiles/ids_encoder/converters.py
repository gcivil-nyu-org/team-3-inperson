from .utils import REGEX
from . import encode_id, decode_id


class HashidsConverter():
    regex = REGEX

    def to_python(self, value: str) -> int:
        return decode_id(value)

    def to_url(self, value: int) -> str:
        return encode_id(value)