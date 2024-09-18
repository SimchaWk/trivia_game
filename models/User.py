from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    id: Optional[int] = None
