import hashlib
from typing import Union

def stable_hash(value: Union[str, bytes]) -> str:
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hashlib.sha256(value).hexdigest()
