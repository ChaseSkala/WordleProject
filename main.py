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
  return response

def gather_information(guess):
  global in_correct_spot
  global in_word_not_spot
  global not_in_word

  letters = list(guess)

  for letter in letters:
    if letter.in_correct_spot():
      in_correct_spot.append(letter)
    elif not letter.in_correct_spot() and letter.in_word():
      in_word_not_spot.append(letter)
    else:
      not_in_word.append(letter)

def main():
  in_correct_spot = []
  in_word_not_spot = []
  not_in_word = []
  session_id = create_session()
  guess = make_guess(session_id)
  gather_information(guess)
main()