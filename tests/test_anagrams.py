import pytest

from puzzle_utils import anagrams as ana


def test_letters_to_primes():
    # E = 2, T = 3, A = 5, so just to be explicit...
    assert ana.letters_to_primes('eat') == 2 * 3 * 5

    assert ana.letters_to_primes('tea') == ana.letters_to_primes('eat')
    assert ana.letters_to_primes('t e a') == ana.letters_to_primes('eat')
    assert ana.letters_to_primes('example') == 109711060


def test_primes_to_letters():
    # Returned string is allcaps, ordered by frequency
    assert ana.primes_to_letters(ana.letters_to_primes('eat')) == 'ETA'

    assert ana.primes_to_letters(109711060) == 'EEALMPX'

    # Some notes on weird inputs
    assert ana.primes_to_letters(-350) == ana.primes_to_letters(350)
    assert ana.primes_to_letters(.5) == ''
    assert ana.primes_to_letters(2 * 131071) == 'E'


def test_anadict(tmp_path):
    wordlist = tmp_path / 'wordlist.txt'
    wordlist.write_text('one\ntwo\nneo\nsyzygy')

    anadict = ana.Anadict.from_path(wordlist)
    one_as_number = ana.letters_to_primes('one')
    assert anadict[one_as_number] == {'ONE', 'NEO'}
    assert anadict['eon'] == {'ONE', 'NEO'}
    assert anadict['two'] == {'TWO'}

    three_as_number = ana.letters_to_primes('three')
    with pytest.raises(KeyError, match=str(three_as_number)):
        _ = anadict[three_as_number]
    with pytest.raises(KeyError, match=str(three_as_number)):
        _ = anadict['ether']
