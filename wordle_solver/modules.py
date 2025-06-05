class LetterInfo:
    in_correct_spot: bool
    in_word: bool
    letter: str

    def __init__(self, in_correct_spot: bool, in_word: bool, letter: str):
        self.in_correct_spot = in_correct_spot
        self.in_word = in_word
        self.letter = letter

class GuessData:
    def __init__(self):
        self.in_correct_spot = [None, None, None, None, None]
        self.in_word_not_spot = []
        self.not_in_word = []
        self.forbidden_spots = {}

    def matches_correct_spots(self, word: str) -> bool:
        for i, letter in enumerate(self.in_correct_spot):
            if letter is not None and word[i] != letter:
                return False
        return True

    def respects_forbidden_spots(self, word: str) -> bool:
        for letter, forbidden_indices in self.forbidden_spots.items():
            for idx in forbidden_indices:
                if idx < len(word) and word[idx] == letter:
                    return False
        return True

    def no_incorrect_letters(self, word: str) -> bool:
        for letter in self.not_in_word:
            if letter in word:
                return False
        return True

    def is_wordle_found(self, word: str):
        for i, letter in enumerate(self.in_correct_spot):
            if letter is None or word[i] != letter:
                return False
        return True

    def use_forbidden_word_in_different_spot(self, word: str) -> bool:
        for letter, forbidden_indices in self.forbidden_spots.items():
            if letter not in word:
                return False
            if all(word[idx] == letter for idx in forbidden_indices):
                return False
        return True

    def filter_words(self, word: str) -> bool:
        return (
                self.matches_correct_spots(word)
                and self.respects_forbidden_spots(word)
                and self.no_incorrect_letters(word)
                and self.use_forbidden_word_in_different_spot(word)
        )

    def gather_information(self, guess: list[LetterInfo]):
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