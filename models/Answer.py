from dataclasses import dataclass
from typing import Optional, Dict

from toolz import get_in


@dataclass
class Answer:
    question_id: int
    incorrect_answer: str
    id: Optional[int] = None
