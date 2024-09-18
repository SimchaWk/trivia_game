from dataclasses import dataclass
from typing import Optional, Dict
from toolz import get_in


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    id: Optional[int] = None

    @classmethod
    def from_api_data(cls, data: Dict) -> 'User':
        return cls(
            first_name=get_in(['name', 'first'], data),
            last_name=get_in(['name', 'last'], data),
            email=get_in(['email'], data),
        )
