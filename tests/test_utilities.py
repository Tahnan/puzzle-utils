import random

import pytest

import puzzle_utils as util


def test_alphafy():
    assert util.alphafy('This: a basic test.') == 'Thisabasictest'
    assert util.alphafy('3. 2 * 2 (!!)') == ''
    assert util.alphafy('a. basic. test.', others=' ') == 'a basic test'


def test_bunch():
    # Strings in, list of strings out
    assert util.bunch('12345678', 4) == ['1234', '5678']
    assert util.bunch('12345678', 3) == ['123', '456', '78']

    # List of strings in, list of lists of strings out
    assert util.bunch(list('12345678'), 4) == [
        ['1', '2', '3', '4'], ['5', '6', '7', '8']
    ]


def test_chunk():
    assert util.chunk('12345678', 2) == ['1234', '5678']
    assert util.chunk('1234567890', 3) == ['1234', '5678', '90']

    # If the string is too short, it does its best
    assert util.chunk('12345678', 5) == ['12', '34', '56', '78']


def test_histogram():
    assert util.histogram('mississippi', printable=False) == {
        4: ['i', 's'], 2: ['p'], 1: ['m']
    }
    assert util.histogram('mississippi') == (
        ' 4: is\n 2: p\n 1: m'
    )


def test_get_enumeration():
    assert util.get_enumeration('wing and a prayer') == '4 3 1 6'
    assert util.get_enumeration('Mr. and Mrs. Smith') == '2. 3 3. 5'

    with_caps = util.get_enumeration('Mr. and Mrs. Smith', show_capitals=True)
    assert with_caps == '*2. 3 *3. *5'

    # Documentation note: internal capitals are not considered
    more_caps = util.get_enumeration('Dr. McMillan of NASA', show_capitals=True)
    assert more_caps == '*2. *8 2 *4'


def test_binarize():
    for _ in range(100):
        # For bases like 2 and 16, this does the same thing as int() and hex(),
        # give or take capitalization and the "0b" or "0x" prefix
        number = random.randint(1, 1000000000)
        assert util.binarize(number) == bin(number)[2:]
        assert util.binarize(number, 16) == hex(number)[2:].upper()

        # For arbitrary bases, on the other hand, there's no built-in reversal
        # of int()
        as_base_25 = int(str(number), 25)
        assert util.binarize(as_base_25, 25) == str(number)

    # Spot check: letters; weird inputs
    assert util.binarize(int('test', 36), 36) == 'TEST'
    assert util.binarize(-32) == '100000'
    assert util.binarize(32.8) == '100000'

    with pytest.raises(ValueError, match='Invalid base'):
        util.binarize(123, 1)

    with pytest.raises(ValueError, match='Invalid base'):
        util.binarize(123, 37)


def test_primefactor():
    assert util.primefactor(32) == [2, 2, 2, 2, 2]
    assert util.primefactor(60) == [2, 2, 3, 5]
    assert util.primefactor(1337) == [7, 191]
    assert util.primefactor(13337) == [13337]


def test_isprime():
    assert util.isprime(2) is True
    assert util.isprime(4) is False
    assert util.isprime(1337) is False
    assert util.isprime(13337) is True


def test_factor():
    assert util.factor(32) == [1, 2, 4, 8, 16, 32]
    assert util.factor(20) == [1, 2, 4, 5, 10, 20]
    assert util.factor(1337) == [1, 7, 191, 1337]


def test_decimate():
    assert util.decimate(3, 6) == [[5], []]  # .5
    assert util.decimate(2, 3) == [[], [6]]  # .6666666...
    assert util.decimate(5, 6) == [[8], [3]]  # .8333333...
    assert util.decimate(1, 7) == [[], [1, 4, 2, 8, 5, 7]]  # .142857142857...

    # Not really intended for improper fractions
    assert util.decimate(15, 8) == [[18, 7, 5], []]  # 1.875
    assert util.decimate(4, 3) == [[13], [3]]  # 1.3333...
