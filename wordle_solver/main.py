import requests
import json
import random

from .modules import LetterInfo
from .modules import GuessData
from .modules import GuessHistory
import importlib.resources

max_attempts = 6

def create_session() -> str:
  """Generates a session id for the user.

  This function contacts the wordle server made by Jordan Mesches at https://github.com/Jordan-Mesches/wordle-server
  and creates a session id for the user that is used to solve the wordle.

  Returns:
    str: The session id for the user.
  """
  url = "http://127.0.0.1:8000/session"

  payload = ""
  headers = {}

  response = requests.request("POST", url, headers=headers, data=payload)
  response.raise_for_status()

  return response.json()['session_id']

def find_new_word(guess_info: GuessData, user_guess: str) -> str:
  """A function that finds a new word to be guessed for the wordle.

  The function takes data from previous guesses and uses that data
  to filter out words and find the next best guess.

  Args:
    guess_info (GuessData): An object containing the current known state
            of the word being guessed, including correct letters, forbidden
            spots, and incorrect letters.

  Returns:
    str: The word that was found to be the next best guess.
  """
  if user_guess is not None:
    found_new_word = False
    with importlib.resources.open_text("wordle_solver", "words.txt") as file:
      words: list[str] = [line.strip() for line in file]
      while not found_new_word:
        if guess_info.in_correct_spot == [None, None, None, None,None] and guess_info.in_word_not_spot == [] and guess_info.not_in_word == []:
          word = user_guess
          found_new_word = True
        else:
          words = list(filter(lambda w: guess_info.filter_words(w), words))
          word: str = random.choice(words)
          found_new_word = True
      return word
  else:
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

def data(word: str, session_id: str) -> dict:
  """A function that holds the web data for the program.

  This function contacts the web url and returns the payload and headers.

  Args:
    word (str): The word to be guessed.
    session_id (str): The session id for the user.

  Returns:
    dict: The payload and headers.
  """
  url = f"http://127.0.0.1:8000/session/{session_id}/guess"
  payload = json.dumps({
    "guess": f"{word}"
  })
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  return response.json()

def make_guess(session_id: str, guess_info: GuessData, user_guess: str) -> tuple[list[LetterInfo], str]:
  """A function that makes the guesses to the wordle server.

  The function takes the next best word and makes a guess
  with the wordle server.

  Args:
    session_id (str): The session id for the user.
    guess_info (GuessData): An object containing the current known state
            of the word being guessed, including correct letters, forbidden
            spots, and incorrect letters.

  Returns:
    A list of the data gained from making the guess and
    the word that was used for making the guess.
  """
  if user_guess is not None:
    word = find_new_word(guess_info, user_guess)
  else:
    word = find_new_word(guess_info, None)
  response = data(word, session_id)
  print(f"Guessed word: {word}")
  print(response)
  letter_infos = []
  for letter_info in response['letters']:
    letter_infos.append(LetterInfo(**letter_info))
  return letter_infos, word

def make_attempt(attempts: int, session_id: str, guess_data: GuessData, user_guess: str) -> tuple[list, str]:
  """A function that makes an attempt at solving the wordle.

  This function makes a guess at solving the wordle and then
  returns the data that was gained from making the guess.

  Args:
    attempts (int): The number of attempts made.
    session_id (str): The session id for the user.
    guess_data (GuessData): An object containing the current known state
            of the word being guessed, including correct letters, forbidden
            spots, and incorrect letters.

  Returns:
    A list of the data used in the guess and the word that was used
    for the guess.
  """
  print(f"Attempt {attempts}")
  if user_guess is not None:
    guess, word = make_guess(session_id, guess_data, user_guess)
    current_state = guess_data.guess_state(guess)
    print(current_state)
  else:
    guess, word = make_guess(session_id, guess_data, None)
    current_state = guess_data.guess_state(guess)
    print(current_state)
  guess_data.gather_information(guess)
  return guess, word


def solve_wordle(user_guess: str) -> tuple[str, int, GuessHistory]:
  """A function that solves the Wordle.

  This function keeps track if the Wordle has been found or not
  and makes attempts using previous guesses and finds the daily Wordle.

  Returns:
      The answer of what the daily Wordle's word is.
  """
  answer = None
  finding_wordle = True
  history = GuessHistory()

  while finding_wordle:
    guess_data = GuessData()
    session_id = create_session()
    attempts = 1
    found_wordle = False
    need_to_exit = False

    guess, word = make_attempt(attempts, session_id, guess_data, user_guess)
    history.add_guess(word, guess)

    while not need_to_exit:
      attempts += 1

      if guess_data.is_wordle_found(word):
        found_wordle = True
        need_to_exit = True
      elif attempts >= max_attempts:
        need_to_exit = True
      else:
        guess, word = make_attempt(attempts, session_id, guess_data, user_guess)
        history.add_guess(word, guess)

    if found_wordle:
      print(f"Today's wordle is {word}")
      finding_wordle = False
      answer = word
    else:
      print("I was unable to find the wordle.")
      print("Re-trying...")

  return answer, attempts, history