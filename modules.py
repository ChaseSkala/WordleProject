class LetterInfo:
    in_correct_spot: bool
    in_word: bool
    letter: str

    def __init__(self, in_correct_spot: bool, in_word: bool, letter: str):
        self.in_correct_spot = in_correct_spot
        self.in_word = in_word
        self.letter = letter

class GuessData:
    in_correct_spot = [None, None, None, None, None]
    in_word_not_spot = []
    not_in_word = []
    forbidden_spots = {}