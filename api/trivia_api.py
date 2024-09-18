import requests
from typing import List, Dict, Any


def fetch_trivia_questions(amount: int = 20) -> List[Dict[str, Any]]:
    api_url = f"https://opentdb.com/api.php?amount={amount}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data['results']
    except requests.RequestException as e:
        print(f"An error occurred while fetching trivia questions: {e}")
        return []
