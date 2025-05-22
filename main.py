import requests
import json
import random

in_correct_spot = []
in_word_not_spot = []
not_in_word = []

def create_session() -> str:
  url = "http://127.0.0.1:8000/session"

  payload = ""
  headers = {}

  response = requests.request("POST", url, headers=headers, data=payload)
  response.raise_for_status()

  return response.json()['session_id']

def make_guess(session_id: str):
  url = f"http://127.0.0.1:8000/session/{session_id}/guess"

  with open('words.txt', 'r') as file:
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
  return response.json()

def gather_information(guess):
  global in_correct_spot
  global in_word_not_spot
  global not_in_word

  data = guess

  for letter_info in data['letters']:
    if letter_info["in_correct_spot"]:
      in_correct_spot.append(letter_info["letter"])
    if letter_info["in_word"] and not letter_info["in_correct_spot"]:
      in_word_not_spot.append(letter_info["letter"])
    if not letter_info["in_word"] and not letter_info["in_correct_spot"]:
      not_in_word.append(letter_info["letter"])

  print(in_correct_spot)
  print(in_word_not_spot)
  print(not_in_word)

def main():
  session_id = create_session()
  guess = make_guess(session_id)
  gather_information(guess)
main()