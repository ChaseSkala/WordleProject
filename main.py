import requests
import json
import random

def create_session() -> str:
  url = "http://127.0.0.1:8000/session"

  payload = ""
  headers = {}

  response = requests.request("POST", url, headers=headers, data=payload)
  response.raise_for_status()
  return response.json()['session_id']

def make_guess(session_id: str):
  url = f"http://127.0.0.1:8000/session/{session_id}/guess"

  with open('../Desktop/New folder/wordle-server/words.txt', 'r') as file:
    words: list[str] = [line.strip() for line in file]
    random_word: str = random.choice(words)

  payload = json.dumps({
    "guess": f"{random_word}"
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)

def main():
  session_id = create_session()
  make_guess(session_id)
main()