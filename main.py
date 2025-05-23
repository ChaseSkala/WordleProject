import requests
import json
import random

from modules import LetterInfo
from modules import GuessData

def create_session() -> str:
  url = "http://127.0.0.1:8000/session"

  payload = ""
  headers = {}

  response = requests.request("POST", url, headers=headers, data=payload)
  response.raise_for_status()

  return response.json()['session_id']

def make_guess(session_id: str, guess_info: GuessData) -> list[LetterInfo]:
  url = f"http://127.0.0.1:8000/session/{session_id}/guess"

  with open('words.txt', 'r') as file:
    words: list[str] = [line.strip() for line in file]
    if guess_info.in_correct_spot == [None, None, None, None, None] and guess_info.in_word_not_spot == [] and guess_info.not_in_word == []:
      word: str = random.choice(words)


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
  return letter_infos

def gather_information(guess: list[LetterInfo], guess_info: GuessData):

  data = guess

  for idx, letter_info in enumerate(data):
    if letter_info.in_correct_spot:
      guess_info.in_correct_spot[idx] = letter_info.letter
    if letter_info.in_word and not letter_info.in_correct_spot:
      for pos, letter_info.letter in enumerate(data):
        if letter_info.letter in guess_info.forbidden_spots:
          guess_info.forbidden_spots.letter.append(pos)
        else:
          guess_info.forbidden_spots[letter_info.letter] = [pos]
    if letter_info.letter in guess_info.in_word_not_spot and letter_info.in_correct_spot:
      guess_info.in_word_not_spot.remove(letter_info.letter)
    if not letter_info.in_word and not letter_info.in_correct_spot:
      guess_info.not_in_word.append(letter_info.letter)

  print(guess_info.in_correct_spot)
  print(guess_info.in_word_not_spot)
  print(guess_info.not_in_word)
  print(guess_info.forbidden_spots)

def main():
  guess_data = GuessData()
  session_id = create_session()
  guess = make_guess(session_id, guess_data)
  gather_information(guess, guess_data)
main()