import requests
import json
import random

from .modules import LetterInfo
from .modules import GuessData
import importlib.resources

max_attempts = 6

def create_session() -> str:
  url = "http://127.0.0.1:8000/session"

  payload = ""
  headers = {}

  response = requests.request("POST", url, headers=headers, data=payload)
  response.raise_for_status()

  return response.json()['session_id']

def find_new_word(guess_info: GuessData):
  found_new_word = False
  with importlib.resources.open_text("wordle_solver", "words.txt") as file:
    words: list[str] = [line.strip() for line in file]
    while not found_new_word:
      if guess_info.in_correct_spot == [None, None, None, None, None] and guess_info.in_word_not_spot == [] and guess_info.not_in_word == []:
        with importlib.resources.open_text("wordle_solver", "startingwords.txt") as file:
          words: list[str] = [line.strip() for line in file]
          word: str = random.choice(words)
        found_new_word = True
      else:
        words = list(filter(lambda w: guess_info.filter_words(w), words))
        word: str = random.choice(words)
        found_new_word = True
    return word

def data(word: str, session_id: str):
  url = f"http://127.0.0.1:8000/session/{session_id}/guess"
  payload = json.dumps({
    "guess": f"{word}"
  })
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  return response.json()

def make_guess(session_id: str, guess_info: GuessData) -> tuple[list[LetterInfo], str]:
  word = find_new_word(guess_info)
  response = data(word, session_id)
  print(f"Guessed word: {word}")
  print(response)
  letter_infos = []
  for letter_info in response['letters']:
    letter_infos.append(LetterInfo(**letter_info))
  return letter_infos, word

def make_attempt(attempts: int, session_id: str, guess_data: GuessData):
  print(f"Attempt {attempts}")
  guess, word = make_guess(session_id, guess_data)
  guess_data.gather_information(guess)
  return guess, word

def solve_wordle():
  answer = None
  finding_wordle = True
  attempts = 1
  found_wordle = False
  need_to_exit = False
  while finding_wordle:
    guess_data = GuessData()
    session_id = create_session()
    guess, word = make_attempt(attempts, session_id, guess_data)
    while not need_to_exit:
      attempts += 1
      if attempts == max_attempts:
        need_to_exit = True
      if guess_data.is_wordle_found(word):
        need_to_exit = True
        found_wordle = True
      else:
        guess, word = make_attempt(attempts, session_id, guess_data)
    if found_wordle:
      print(f"Today's wordle is {word}")
      finding_wordle = False
      answer = word
    else:
      print("I was unable to find the wordle.")
      print("Re-trying...")
  return answer

def main():
  wordle_answer = solve_wordle()
  print(wordle_answer)