class LetterInfo:
    in_correct_spot: bool
    in_word: bool
    letter: str

    def __init__(self, in_correct_spot: bool, in_word: bool, letter: str):
        self.in_correct_spot = in_correct_spot
        self.in_word = in_word
        self.letter = letter

class LetterState:
    def __init__(self, letter_info):
        self.letter = letter_info.letter
        if letter_info.in_correct_spot:
            self.status = "green"
        elif letter_info.in_word:
            self.status = "yellow"
        else:
            self.status = "red"

    def to_dict(self):
        return {
            "letter": self.letter,
            "status": self.status
        }

class GuessState:
    def __init__(self, word: str, letter_infos: list):
        self.word = word
        self.result = [LetterState(li) for li in letter_infos]

    def to_dict(self):
        return {
            "word": self.word,
            "result": [letter.to_dict() for letter in self.result]
        }

class GuessHistory:
    def __init__(self):
        self.guesses: list[GuessState] = []

    def add_guess(self, word: str, letter_infos: list):
        self.guesses.append(GuessState(word, letter_infos))

    def to_dict(self):
        return {
            "guesses": [guess.to_dict() for guess in self.guesses]
        }

class GuessData:
    def __init__(self):
        self.in_correct_spot = [None, None, None, None, None]
        self.in_word_not_spot = []
        self.not_in_word = []
        self.forbidden_spots = {}
        self.current_guess_state = []

    def matches_correct_spots(self, word: str) -> bool:
        """Makes sure that the letters are in the correct spots.

        It makes sure if the value of the list in_correct_spot is
        not None, and checks to see if the correct value is inside of
        that spot. If it is not, then it returns false; otherwise True.

        Args:
          word (str): The word to be checked.

        Returns:
            A value that decides if the correct letters are in the correct spots.
        """
        for i, letter in enumerate(self.in_correct_spot):
            if letter is not None and word[i] != letter:
                return False
        return True

    def respects_forbidden_spots(self, word: str) -> bool:
        """Makes sure that a letter cannot be in the same spot twice

        Checks to make sure that a letter that is in the word
        but not in a certain spot isn't in that spot.

        Args:
          word (str): The word to be checked.

        Returns:
            A value that decides if the letter is in the same spot twice.
        """
        for letter, forbidden_indices in self.forbidden_spots.items():
            for idx in forbidden_indices:
                if idx < len(word) and word[idx] == letter:
                    return False
        return True

    def no_incorrect_letters(self, word: str) -> bool:
        """Makes sure that no incorrect letters are used again

        Checks to see if an incorrect letter is in the next guessed
        word. If it is then it returns False; otherwise True.

        Args:
          word (str): The word to be checked.

        Returns:
          A value that decides if the incorrect letter is in the next guessed
        """
        for letter in self.not_in_word:
            if letter in word:
                return False
        return True

    def is_wordle_found(self, word: str) -> bool:
        """Checks to see if the wordle was found or not.

        Checks each letter in the list in_correct_spot is
        correct. If each individual letter is not in the
        correct spot, it returns False; otherwise True.

        Args:
          word (str): The word to be checked.

        Returns:
          A value that decides if the wordle is found or not.
        """
        for i, letter in enumerate(self.in_correct_spot):
            if letter is None or word[i] != letter:
                return False
        return True

    def use_forbidden_word_in_different_spot(self, word: str) -> bool:
        """Makes sure that a letter is used in a different spot in the next word guessed.

        Checks to see if a letter that is in the word but the
        incorrect spot is used in a different spot in the next
        word guessed.

        Args:
          word (str): The word to be checked.

        Returns:
          A value that decides if the next word guessed has forbidden letters in different spots
        """
        for letter, forbidden_indices in self.forbidden_spots.items():
            if letter not in word:
                return False
            if all(word[idx] == letter for idx in forbidden_indices):
                return False
        return True

    def filter_words(self, word: str) -> bool:
        """Filters out words that can be chosen for the next guess.

        Filters out the next possible words to be chosen for a guess
        based on the results of matches_correct_spots, respects_forbidden_spots,
        no_incorrect_letters, and respects_forbidden_word_in_different_spot.

        Args:
          word (str): The word to be checked.

        Returns:
          A value that represents if the next word has been filtered.
        """
        return (
                self.matches_correct_spots(word)
                and self.respects_forbidden_spots(word)
                and self.no_incorrect_letters(word)
                and self.use_forbidden_word_in_different_spot(word)
        )

    def gather_information(self, guess: list[LetterInfo]):
        """Gathers information based on results of guesses.

        Uses information based on the results of previous guesses
        and uses that data to sort and give values to the lists
        used for the next guess.

        Args:
          guess (list[LetterInfo]): The results of previous guesses.

        """
        for idx, letter_info in enumerate(guess):
            if letter_info.in_correct_spot:
                self.in_correct_spot[idx] = letter_info.letter
            if letter_info.in_word and not letter_info.in_correct_spot:
                if letter_info.letter in self.forbidden_spots:
                    self.forbidden_spots[letter_info.letter].append(idx)
                else:
                    self.forbidden_spots[letter_info.letter] = [idx]
            if letter_info.letter in self.in_word_not_spot and letter_info.in_correct_spot:
                self.in_word_not_spot.remove(letter_info.letter)
            if not letter_info.in_word and not letter_info.in_correct_spot:
                if letter_info.letter not in self.not_in_word:
                    self.not_in_word.append(letter_info.letter)

        print(self.in_correct_spot)
        print(self.in_word_not_spot)
        print(self.forbidden_spots)
        print(self.not_in_word)