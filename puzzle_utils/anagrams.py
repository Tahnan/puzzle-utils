"""
Anagram utilities.

Representing letters as primes and words as their product is not original to
me, but I stol...er, "borrowed" the idea so long ago that I can't for the life
of me remember whose it was.
"""
# Letters ordered by frequency, mapped to the first 26 primes
LETTERS_TO_PRIMES = {
    'E': 2,  'T': 3,  'A': 5,  'O': 7,  'I': 11, 'N': 13, 'S': 17, 'R': 19,
    'H': 23, 'L': 29, 'D': 31, 'C': 37, 'U': 41, 'M': 43, 'F': 47, 'P': 53,
    'G': 59, 'W': 61, 'Y': 67, 'B': 71, 'V': 73, 'K': 79, 'X': 83, 'J': 89,
    'Q': 97, 'Z': 101
}
PRIMES_TO_LETTERS = {y: x for x, y in LETTERS_TO_PRIMES.items()}


def letters_to_primes(word):
    """
    Given a word, convert it to its numeric representation.  ("Primes" here is
    shorthand for "product of primes", i.e., number, but it's a less generic
    name than "letters_to_number" would be.)
    """
    result = 1
    for letter in word.upper():
        result *= LETTERS_TO_PRIMES.get(letter, 1)
    return result


def primes_to_letters(number):
    """
    Given a number, convert it to a letter string.  (See above re the name.)
    """
    result = ''
    for prime in PRIMES_TO_LETTERS:
        while not number % prime:
            number //= prime
            result += PRIMES_TO_LETTERS[prime]
        if number == 1:
            break
    return result


class Anadict(dict):
    """
    Dictionary that allows lookup by integer or string.
    """
    @classmethod
    def from_path(cls, path):
        """
        Given a path, return an Anadict of lines from that path (i.e. one that
        maps numbers to the lines in the file that correspond to that number).
        """
        anadict = {}
        with open(path) as f:
            for line in f:
                line = line.strip().upper()
                anadict.setdefault(letters_to_primes(line), set()).add(line)
        return cls(anadict)

    def __getitem__(self, item):
        if isinstance(item, str):
            item = letters_to_primes(item)
        return super().__getitem__(item)
