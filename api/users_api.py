import requests
from typing import List, Dict, Any


def fetch_users(amount: int = 4) -> List[Dict[str, Any]]:
    api_url = f"https://randomuser.me/api?results={amount}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data['results']
    except requests.RequestException as e:
        print(f"An error occurred while fetching random users: {e}")
        return []
