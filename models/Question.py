from dataclasses import dataclass
from typing import Optional, Dict
from toolz import get_in


@dataclass
class Question:
    question_text: str
    correct_answer: str
    id: Optional[int] = None

    @classmethod
    def from_api_data(cls, data: Dict) -> 'Question':
        return cls(
            question_text=get_in(['question'], data),
            correct_answer=get_in(['correct_answer'], data)
        )
