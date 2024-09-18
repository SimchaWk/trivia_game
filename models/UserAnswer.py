from dataclasses import dataclass
from typing import Optional
from datetime import timedelta


@dataclass
class UserAnswer:
    user_id: int
    question_id: int
    answer_text: str
    is_correct: bool
    time_taken: timedelta
    id: Optional[int] = None
