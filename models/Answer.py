from dataclasses import dataclass
from typing import Optional


@dataclass
class Answer:
    question_id: int
    incorrect_answer: str
    id: Optional[int] = None
