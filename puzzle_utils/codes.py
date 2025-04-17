"""
Enciphering classes.

(Or "encodings" except that "string encoding" is already a thing.)

The main entry for each class is the `encode()` and `decode()` pair.
"""
from string import ascii_uppercase, ascii_lowercase

from puzzle_utils import bunch, alphafy
from puzzle_utils import data


class Atbash:
    """
    The Atbash is a simple substitution cipher in which A=Z, B=Y, ..., Z=A.
    """
    def __init__(self):
        self.translation = {65 + x: 90 - x for x in range(26)}
        self.translation.update({97 + x: 122 - x for x in range(26)})

    def decode(self, text):
        """
        Run a string through the Atbash encoding.
        """
        return text.translate(self.translation)

    # Atbash is symmetric, so encoding is the same as decoding
    encode = decode


class Caesar:
    def __init__(self):
        # These could be made on the fly, but `show_all()` is enough of a use
        # case that it's nice to have them all calculated in advance
        self.translations = {}
        for i in range(26):
            self.translations[i] = str.maketrans(
                ascii_uppercase + ascii_lowercase,
                (ascii_uppercase[i:] + ascii_uppercase[:i] +
                 ascii_lowercase[i:] + ascii_lowercase[:i])
            )

    def encode(self, text, distance):
        return text.translate(self.translations[distance % 26])

    def decode(self, text, distance):
        return text.translate(self.translations[(26 - distance) % 26])

    def show_all(self, text):
        return [text.translate(self.translations[i]) for i in range(26)]


class _LookupCode:
    """
    A class not meant to be instantiated on its own, but to serve as the
    superclass for lookup-dictionary-based codes.
    """
    _letter_to_code = {}
    _code_to_letter = {}

    @classmethod
    def encode(cls, text):
        return [cls._letter_to_code.get(ltr, '?')
                for ltr in alphafy(text).upper()]

    @classmethod
    def decode(cls, text):
        return [cls._letter_to_code.get(ltr, '?')
                for ltr in alphafy(text).upper()]


class Bacon:
    """
    The Bacon cipher is a binary-like encoding of letters.
    """
    # The reason we need a Bacon class and not classes for other dictionary
    # mappings like Braille is that Bacon ciphers usually need a function to
    # indicate what is "a" and what is "b".
    def __init__(self, ab_function=None):
        # "ab_function" should be a function that returns "a" or "b", and may
        # raise a ValueError for ill-defined inputs
        self.ab_function = ab_function or self.default_ab

    @staticmethod
    def default_ab(letter):
        if letter in ('a', 'b'):
            return letter
        raise ValueError(f'Neither a nor b: {letter}')

    @classmethod
    def as_binary(cls):
        def bin_ab(digit):
            if digit == '1':
                return 'b'
            if digit == '0':
                return 'a'
            raise ValueError(f'Neither 0 nor 1: {digit}')

        return cls(ab_function=bin_ab)

    def decode(self, ciphertext):
        """
        Decodes ciphertext as a Bacon cipher.  Ciphertext must be an iterable
        of individual bits.
        """
        plaintext = ''
        for bits in bunch(ciphertext, 5):
            baconized = ''.join([self.ab_function(b) for b in bits])
            plaintext += data.BACON_TO_LETTER.get(baconized, '?')
        return plaintext


class Playfair:
    def __init__(self, keyword):
        self._coords_to_letters = {}
        self._letters_to_coords = {}
        alphabet = (keyword.upper() + ascii_uppercase).replace('J', 'I')
        coordinate = 0
        for letter in alphabet:
            if letter.isalpha() and letter not in self._letters_to_coords:
                coord = divmod(coordinate, 5)
                self._letters_to_coords[letter] = coord
                self._coords_to_letters[coord] = letter
                coordinate += 1

    @staticmethod
    def _pad(letter):
        # Small helper function to turn a single letter into a bigram, which
        # would just be "add 'X'" if it weren't for X itself
        return letter + ('Q' if letter == 'X' else 'X')

    def _translate(self, text, direction):
        """
        Given a text and a direction, run it through the Playfair cipher.
        "Direction" is 1 for encoding, -1 for decoding.
        """
        bigrams = bunch(alphafy(text.upper()).replace('J', 'I'), 2)
        result = []

        # Rather than looping through bigrams, we do this as a while loop, so
        # that padding can be added as we go
        while bigrams:
            pair = bigrams.pop(0)
            if len(pair) == 1:
                pair = self._pad(pair)
            a, b = pair
            if a == b:
                # If we need to add a padding letter, it'll realign all the
                # subsequent pairs, so reset "bigrams" and restart the loop
                bigrams = bunch(self._pad(a) + b + ''.join(bigrams), 2)
                continue

            ax, ay = self._letters_to_coords[a]
            bx, by = self._letters_to_coords[b]
            if ax == bx:
                ay = (ay + direction) % 5
                by = (by + direction) % 5
            elif ay == by:
                ax = (ax + direction) % 5
                bx = (bx + direction) % 5
            else:
                ay, by = by, ay
            result.append(self._coords_to_letters[(ax, ay)])
            result.append(self._coords_to_letters[(bx, by)])
        return ''.join(result)

    def encode(self, text):
        """
        Given plaintext, encode it using the Playfair cipher.
        """
        return self._translate(text, 1)

    def decode(self, text):
        """
        Given ciphertext, decode it using the Playfair cipher.
        """
        return self._translate(text, -1)
