from dataclasses import dataclass
from typing import Optional


@dataclass
class Question:
    question_text: str
    correct_answer: str
    id: Optional[int] = None
