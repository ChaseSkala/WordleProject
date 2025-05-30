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

def matches_correct_spots(word, guess_info):
  for i, letter in enumerate(guess_info.in_correct_spot):
    if letter is not None and word[i] != letter:
      return False
  return True

def respects_forbidden_spots(word: str, guess_info: GuessData) -> bool:
  for letter, forbidden_indices in guess_info.forbidden_spots.items():
    for idx in forbidden_indices:
      if idx < len(word) and word[idx] == letter:
        return False
  return True

def no_incorrect_letters(word: str, guess_info: GuessData) -> bool:
  for letter in guess_info.not_in_word:
    if letter in word:
      return False
  return True


def is_wordle_found(word, guess_info):
  for i, letter in enumerate(guess_info.in_correct_spot):
    if letter is None or word[i] != letter:
      return False
  return True

def filter_words(word: str, guess_info: GuessData) -> bool:
  return matches_correct_spots(word, guess_info) and respects_forbidden_spots(word, guess_info) and no_incorrect_letters(word, guess_info)

def make_guess(session_id: str, guess_info: GuessData) -> tuple[list[LetterInfo], str]:
  url = f"http://127.0.0.1:8000/session/{session_id}/guess"

  found_new_word = False

  with open('words.txt', 'r') as file:
    words: list[str] = [line.strip() for line in file]
    while not found_new_word:
      if guess_info.in_correct_spot == [None, None, None, None, None] and guess_info.in_word_not_spot == [] and guess_info.not_in_word == []:
        word: str = random.choice(words)
        found_new_word = True
      else:
        words = list(filter(lambda w: filter_words(w, guess_info), words))
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

def gather_information(guess: list[LetterInfo], guess_info: GuessData):
  for idx, letter_info in enumerate(guess):
    if letter_info.in_correct_spot:
      guess_info.in_correct_spot[idx] = letter_info.letter
    if letter_info.in_word and not letter_info.in_correct_spot:
      if letter_info.letter in guess_info.forbidden_spots:
        guess_info.forbidden_spots[letter_info.letter].append(idx)
      else:
        guess_info.forbidden_spots[letter_info.letter] = [idx]
    if letter_info.letter in guess_info.in_word_not_spot and letter_info.in_correct_spot:
      guess_info.in_word_not_spot.remove(letter_info.letter)
    if not letter_info.in_word and not letter_info.in_correct_spot:
      if letter_info.letter not in guess_info.not_in_word:
        guess_info.not_in_word.append(letter_info.letter)

  print(guess_info.in_correct_spot)
  print(guess_info.in_word_not_spot)
  print(guess_info.forbidden_spots)
  print(guess_info.not_in_word)

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
    gather_information(guess, guess_data)
    while not ready_to_exit:
      attempts += 1
      if attempts == max_attempts:
        ready_to_exit = True
      if is_wordle_found(word, guess_data):
        ready_to_exit = True
        found_wordle = True
      else:
        print(f"Attempt {attempts}")
        guess, word = make_guess(session_id, guess_data)
        gather_information(guess, guess_data)
    if found_wordle:
      print(f"Today's wordle is {word}")
      finding_wordle = False
    else:
      print("I was unable to find the wordle.")
      print("Re-trying...")
main()