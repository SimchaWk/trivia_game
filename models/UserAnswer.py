from dataclasses import dataclass
from typing import Optional, Dict
from datetime import timedelta

from toolz import get_in


@dataclass
class UserAnswer:
    user_id: int
    question_id: int
    answer_text: str
    is_correct: bool
    time_taken: timedelta
    id: Optional[int] = None
