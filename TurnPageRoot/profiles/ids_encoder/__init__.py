from .utils import PARAMS
from hashids import Hashids

hashids = Hashids(**PARAMS)

def encode_id(_id: int) -> str:
    return hashids.encode(_id)

def decode_id(_id: str) -> int:
    decoded_values = hashids.decode(_id)
    # output of hashids.decode is always a tuple
    if len(decoded_values) != 1:
        raise ValueError
    return decoded_values[0]