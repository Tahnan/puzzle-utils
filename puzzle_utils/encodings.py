from puzzle_utils import data


def _decode(message, dictionary):
    """
    Given a message (as a space-separated string, or a list of strings) and a
    decoding dictionary, return a plaintext string.
    """
    if isinstance(message, str):
        message = message.split()
    return ''.join([dictionary.get(x, '?') for x in message])


# Three popular puzzle encodings: Braille, Morse, semaphore
def braille(message):
    """Convert a Braille message to plain text."""
    return _decode(message, data.BRAILLE_TO_LETTER)


def morse(message):
    """Convert a Morse message to plain text."""
    # By habit, I often represent Morse separated by slashes
    message = message.replace('/', ' ')
    return _decode(message, data.MORSE_TO_LETTER)


def semaphore(message):
    """Convert a semaphore message to plain text."""
    return _decode(message, data.SEMAPHORE_TO_LETTER)


def scrabble(word):
    """Convert a word to its point value in Scrabble."""
    return sum([data.SCRABBLE_VALUES.get(letter, 0) for letter in word.upper()])
