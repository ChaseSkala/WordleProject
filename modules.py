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

    def matches_correct_spots(word: str) -> bool:
        for i, letter in enumerate(GuessData.in_correct_spot):
            if letter is not None and word[i] != letter:
                return False
        return True

    def respects_forbidden_spots(word: str) -> bool:
        for letter, forbidden_indices in GuessData.forbidden_spots.items():
            for idx in forbidden_indices:
                if idx < len(word) and word[idx] == letter:
                    return False
        return True

    def no_incorrect_letters(word: str) -> bool:
        for letter in GuessData.not_in_word:
            if letter in word:
                return False
        return True

    def is_wordle_found(word: str):
        for i, letter in enumerate(GuessData.in_correct_spot):
            if letter is None or word[i] != letter:
                return False
        return True

    def use_forbidden_word_in_different_spot(word: str) -> bool:
        for letter, forbidden_indices in GuessData.forbidden_spots.items():
            if letter not in word:
                return False
            if all(word[idx] == letter for idx in forbidden_indices):
                return False
        return True

    def filter_words(word: str) -> bool:
        return (
                GuessData.matches_correct_spots(word)
                and GuessData.respects_forbidden_spots(word)
                and GuessData.no_incorrect_letters(word)
                and GuessData.use_forbidden_word_in_different_spot(word)
        )

    def gather_information(guess: list[LetterInfo]):
        for idx, letter_info in enumerate(guess):
            if letter_info.in_correct_spot:
                GuessData.in_correct_spot[idx] = letter_info.letter
            if letter_info.in_word and not letter_info.in_correct_spot:
                if letter_info.letter in GuessData.forbidden_spots:
                    GuessData.forbidden_spots[letter_info.letter].append(idx)
                else:
                    GuessData.forbidden_spots[letter_info.letter] = [idx]
            if letter_info.letter in GuessData.in_word_not_spot and letter_info.in_correct_spot:
                GuessData.in_word_not_spot.remove(letter_info.letter)
            if not letter_info.in_word and not letter_info.in_correct_spot:
                if letter_info.letter not in GuessData.not_in_word:
                    GuessData.not_in_word.append(letter_info.letter)

        print(GuessData.in_correct_spot)
        print(GuessData.in_word_not_spot)
        print(GuessData.forbidden_spots)
        print(GuessData.not_in_word)