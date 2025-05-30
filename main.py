import requests
import json
import random

from modules import LetterInfo
from modules import GuessData

max_attempts = 6

def create_session() -> str:
  url = "http://127.0.0.1:8000/session"

  payload = ""
  headers = {}

  response = requests.request("POST", url, headers=headers, data=payload)
  response.raise_for_status()

  return response.json()['session_id']

def make_guess(session_id: str, guess_info: GuessData) -> tuple[list[LetterInfo], str]:
  url = f"http://127.0.0.1:8000/session/{session_id}/guess"

  found_new_word = False

  with open('words.txt', 'r') as file:
    words: list[str] = [line.strip() for line in file]
    while not found_new_word:
      if guess_info.in_correct_spot == [None, None, None, None, None] and guess_info.in_word_not_spot == [] and guess_info.not_in_word == []:
        with open('startingwords.txt', 'r') as file:
          words: list[str] = [line.strip() for line in file]
          word: str = random.choice(words)
        found_new_word = True
      else:
        words = list(filter(lambda w: GuessData.filter_words(w), words))
        word: str = random.choice(words)
        found_new_word = True

  payload = json.dumps({
    "guess": f"{word}"
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  print(f"Guessed word: {word}")
  print(response.text)
  response = response.json()
  letter_infos = []
  for letter_info in response['letters']:
    letter_infos.append(LetterInfo(**letter_info))
  return letter_infos, word

def main():
  finding_wordle = True
  while finding_wordle:
    attempts = 1
    found_wordle = False
    ready_to_exit = False
    guess_data = GuessData()
    session_id = create_session()
    print(f"Attempt {attempts}")
    guess, word = make_guess(session_id, guess_data)
    GuessData.gather_information(guess)
    while not ready_to_exit:
      attempts += 1
      if attempts == max_attempts:
        ready_to_exit = True
      if GuessData.is_wordle_found(word):
        ready_to_exit = True
        found_wordle = True
      else:
        print(f"Attempt {attempts}")
        guess, word = make_guess(session_id, guess_data)
        GuessData.gather_information(guess)
    if found_wordle:
      print(f"Today's wordle is {word}")
      finding_wordle = False
    else:
      print("I was unable to find the wordle.")
      print("Re-trying...")
main()