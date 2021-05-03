"""Project 1 - Phrase Puzzler Program"""
#author: Muntaqa Mahmood

from project1_constants import (CONSONANT_POINTS, VOWEL_PRICE, CONSONANT_BONUS,
                       PLAYER_ONE, PLAYER_TWO, CONSONANT, VOWEL,
                       SOLVE, QUIT, HUMAN, HUMAN_HUMAN,
                       HUMAN_COMPUTER, EASY, HARD, ALL_CONSONANTS,
                       ALL_VOWELS, PRIORITY_CONSONANTS, HIDDEN)

def is_win(puzzle: str, view: str) -> bool:
    """Return True if and only if puzzle and view are a winning
    combination. That is, if and only if puzzle and view are the same.

    >>> is_win('banana', 'banana')
    True
    >>> is_win('apple', 'a^^le')
    False
    >>> is_win('apple', 'app')
    False
    """

    return puzzle == view

def is_game_over(puzzle: str, view: str, move: str) -> bool:
    """Return True if and only if puzzle and view are a winning
    combination or move is QUIT.

    >>> is_game_over('apple', 'a^^le', 'V')
    False
    >>> is_game_over('apple', 'a^^le', 'Q')
    True
    >>> is_game_over('apple', 'apple', 'S')
    True
    """

    return move == QUIT or is_win(puzzle, view)


def is_one_player_game(game_type: str) -> bool:
    """Return True if and only if it is a one-player game.
    For this to be true, game_type and constant HUMAN have
    to be the same.

    >>> is_one_player_game('H-')
    True
    >>> is_one_player_game('HH')
    False
    >>> is_one_player_game('HC')
    False

    """

    return game_type == HUMAN

def is_human(current_player: str, game_type: str) -> bool:
    """Return True if and only if current_player represents a human in a
    game of type game_type.

    current_player is PLAYER_ONE or PLAYER_TWO.
    game_type is HUMAN, HUMAN_HUMAN, or HUMAN_COMPUTER.

    In a HUMAN game or a HUMAN_HUMAN game, a player is always
    human. In a HUMAN_COMPUTER game, PLAYER_ONE is human and
    PLAYER_TWO is computer.

    >>> is_human('Player One', 'H-')
    True
    >>> is_human('Player One', 'HH')
    True
    >>> is_human('Player Two', 'HH')
    True
    >>> is_human('Player One', 'HC')
    True
    >>> is_human('Player Two', 'HC')
    False
    """

    return game_type != HUMAN_COMPUTER or current_player == PLAYER_ONE

def half_revealed(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic
    characters in view are revealed.

    >>> half_revealed('')
    True
    >>> half_revealed('x')
    True
    >>> half_revealed('^')
    False
    >>> half_revealed('a^,^c!')
    True
    >>> half_revealed('a^b^^e ^c^d^^d')
    False
    """

    num_hidden = view.count(HIDDEN)
    num_alphabetic = 0
    for char in view:
        if char.isalpha():
            num_alphabetic += 1
    return num_alphabetic >= num_hidden


def current_player_score(player_one_score: int, player_two_score: int,
                         current_player: str) -> int:
    """Return the score of the current player. That is, if and only if
    current_player is the same as PLAYER_ONE or else return player_two_score.

    >>> current_player_score(3, 2, 'Player Two')
    2
    >>> current_player_score(6, 5, 'Player One')
    6
    """

    if current_player == PLAYER_ONE:

        return player_one_score

    return player_two_score


def is_bonus_letter(letter: str, puzzle: str, view: str) -> bool:
    """Return True if and only if first argument is a bonus letter.
    Bonus letters are currently hidden consonants. If and only if bonus letter
    is included in HIDDEN.

    >>> is_bonus_letter('v', 'science', '^^^^^^^')
    False
    >>> is_bonus_letter('c', 'computer', '^^^^^^^^')
    True

    """

    return letter in ALL_CONSONANTS and letter in puzzle and\
           view[puzzle.index(letter)] == HIDDEN


def update_char_view(puzzle: str, view: str, char_index: int,
                     guess: str) -> str:
    """Return function with what the updated view of the character should be.
    If the guess is correct, reveal the character. Incorrect guess should not
    change the view.

    >>> update_char_view('apple', '^^^^^', 3, 'l')
    'l'
    >>> update_char_view('banana', '^^^^^^', 4, 'z')
    '^'
    """

    if view[char_index] != HIDDEN:
        return view[char_index]

    elif puzzle[char_index] == guess:
        return guess

    else:
        return HIDDEN


def calculate_score(current_score: int, revealed_occurrences: int,
                    current_move: str) -> int:
    """Return current_score updated and current_score increases with guessing
    consonants depending on the revealed_occurrences and buying vowels decreases
    the score accordingly.

    >>> calculate_score(2, 2, 'V')
    1
    >>> calculate_score(1, 0, 'C')
    1
    >>> calculate_score(3, 2, 'C')
    5
    """

    if current_move == CONSONANT:
        current_score = current_score + revealed_occurrences * CONSONANT_POINTS

    elif current_move == VOWEL:
        current_score = current_score - VOWEL_PRICE

    return current_score


def next_player(current_player: str, revealed_occurrences: int,
                game_type: str) -> str:
    """Return Player One or Player Two to play in the next turn.
    If current_player correctly guesses a consonant or buys a vowel that occurs
    in the puzzle, then current_player goes again. If current_player guesses
    incorrectly, the other player goes in the next turn.

    >>> next_player('Player One', 0, 'HH')
    'Player Two'
    >>> next_player('Player One', 1, "HH")
    'Player One'

    """

    if game_type == HUMAN:
        return PLAYER_ONE

    elif current_player == PLAYER_TWO and revealed_occurrences == 0:
        return PLAYER_ONE

    elif current_player == PLAYER_ONE and revealed_occurrences == 0:
        return PLAYER_TWO

    elif current_player == PLAYER_ONE and revealed_occurrences > 0:
        return PLAYER_ONE

    elif current_player == PLAYER_TWO and revealed_occurrences > 0:
        return PLAYER_TWO

    return PLAYER_ONE


def is_hidden(index: int, puzzle: str, view: str) -> bool:
    """Return True if and only if the character is hidden at index. HIDDEN
    character cannot be revealed at any position in view. Otherwise, if
    index does not match with the view position then it is False.

    >>> is_hidden(3, 'banana', 'ban^na')
    True
    >>> is_hidden(2, 'apple', '^pple')
    False
    """

    return puzzle[index] != view[index] and view[index] == HIDDEN


def computer_chooses_solve(view: str, difficulty: str,
                           not_yet_guessed_consonants: str) -> bool:
    """Return True if and only if the computer decides to solve the puzzle.

    If difficulty is H, computer chooses to solve the puzzle if half of the
    characters are revealed or if no more not_yet_guessed_consonants are left
    to guess.

    If difficulty is E, computer chooses to solve if not_yet_guessed_consonants
    value is none. Else, the computer does not choose to solve.

    >>> computer_chooses_solve('sc^^nc^', 'H', '0')
    True
    >>> computer_chooses_solve('^^^^^^^', 'H', '4')
    False

    """

    if len(not_yet_guessed_consonants) == 0:
        return True

    elif difficulty == HARD:
        return not_yet_guessed_consonants == 0 or half_revealed(view)

    return False


def erase(string_letters: str, string_index: int) -> str:
    """Return the string_letters with the character at the string_index removed
    if the string_index is between range 0 and the last string_index.
    Otherwise return the original string_letters unchanged.

    >>> erase('assignment', 4)
    'assinment'
    >>> erase('assignment', 13)
    'assignment'

    """

    if string_index in range(0, len(string_letters)):
        return string_letters[:string_index] + string_letters[string_index + 1:]

    else:
        return string_letters


if __name__ == '__main__':
    import doctest
    doctest.testmod()
