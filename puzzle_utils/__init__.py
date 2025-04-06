import itertools
import operator
import re
from collections import defaultdict
from functools import reduce
from math import ceil


# Language Functions

def alphafy(to_alphafy, others=''):
    """
    Given a string, return the string with non-letters removed. (Optionally
    keep other characters with `others`.)
    """
    return ''.join(z for z in to_alphafy if z.isalpha() or z in others)


# Replaceable by itertools.batch, perhaps, though this has the advantage that
# its output is a list of its input type: a list of strings becomes a list of
# lists of strings; a string becomes a list of strings; etc.
def bunch(iterable, length):
    """
    Breaks a text into a list of pieces of the given length.  For example:

    >>> bunch("forexample", 3)
    ['for', 'exa', 'mpl', 'e']
    """
    result = [iterable[x * length:(x + 1) * length]
              for x in range(1 + len(iterable) // length)]
    return [x for x in result if x]


def chunk(text, howmany):
    """
    Breaks a text into a list of the given number of pieces of equal length.
    For example:

    >>> chunk("forexample", 3)
    ['fore', 'xamp', 'le']
    """
    return bunch(text, ceil((len(text) - .5) / howmany))


def histogram(text, printable=True):
    """
    Given a text, returns a histogram of the text.  By default, this is a
    printable string, but if `printable` is False, it will be a dictionary
    mapping an integer to a list of characters with that count.
    """
    histodict = defaultdict(list)

    for character in sorted(set(text)):
        histodict[text.count(character)].append(character)
    if not printable:
        return dict(histodict)

    to_print = [f'{count:>2}: {"".join(chars)}'
                for count, chars in sorted(histodict.items(), reverse=True)]
    return '\n'.join(to_print)


def get_enumeration(answer, show_capitals=False):
    """
    Given a phrase, return its enumeration (i.e., with each word replaced by
    the number of letters in the word), preserving spacing and punctuation.
    If `show_capitals` is True, will add an "*" before each capitalized word.
    """
    # Note: Internal capitals are not considered.  "NASA" will produce "*4"
    # (and not "*1*1*1*1 or **4, two traditional ways of representing an
    # an all-caps string); "McMillan" will produce "*8" and not "*2*6".  In
    # practical terms, I never need that level of precision; mostly I just need
    # help counting.
    enumeration = ''
    for piece in re.findall(r'(\W+|\w+)', answer):
        if piece.isalpha():
            if show_capitals and piece[0].isupper():
                enumeration += '*'
            enumeration += str(len(piece))
        else:
            enumeration += piece
    return enumeration


# Math Functions

def binarize(number, base=2):
    """
    Takes a number and optionally a base (default 2), and returns a string that
    represents that number in that base.  `base` must be between 2 and 36
    inclusive.
    """
    if base < 2 or base > 36:
        raise ValueError('Invalid base')
    number = int(abs(number))   # gives screwy results for bad inputs
    if number == 0:
        return '0'
    result = ''
    while number:
        result = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[number % base] + result
        number = number // base
    return result


def primefactor(num):
    """
    Given a number, returns a list of its prime factors (increasing)

    >>> primefactor(5551212)
    [2, 2, 3, 73, 6337]
    """
    primefactors = []
    n = 2
    while n <= num ** .5 + 1:
        while not num % n:
            num //= n
            primefactors.append(n)
            if num == 1:
                return primefactors
        n += (1 if n == 2 else 2)
    primefactors.append(num)
    return primefactors


def isprime(num):
    """
    Returns True if num is prime, False otherwise.  Faster than primefactor
    if you just need a yes-or-no.
    """
    if num < 2:
        return False
    if num > 2 and not num % 2:
        return False
    for k in range(3, int(num ** .5) + 1, 2):
        if not num % k:
            return False
    return True


def factor(n):
    pfs = primefactor(n)
    pf_and_es = [(x, pfs.count(x)) for x in set(pfs)]
    factors = []
    powerlist = [[pf ** n for n in range(ex + 1)] for pf, ex in pf_and_es]
    for p in itertools.product(*powerlist):
        factors.append(reduce(operator.mul, p))
    factors.sort()
    return factors


def decimate(num, denom):
    expansion = []
    numseen = []
    while num not in numseen and num != 0:
        numseen.append(num)
        num *= 10
        exp, num = divmod(num, denom)
        expansion.append(exp)
    if num == 0:
        result = [expansion, []]
    else:
        break_point = numseen.index(num)
        result = [expansion[:break_point], expansion[break_point:]]
    return result
