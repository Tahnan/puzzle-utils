from puzzle_utils import encodings as enc


def test_decode():
    # Some tests for the underlying decoder
    code = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'}
    assert enc._decode('3 1 2', code) == 'CAB'
    assert enc._decode(['3', '1', '2'], code) == 'CAB'
    assert enc._decode('3 8 2', code) == 'C?B'


def test_braille():
    example = '*...*. *.**.* *..... *.**.. ****.. ***... *...*.'
    assert enc.braille(example) == 'EXAMPLE'


def test_morse():
    assert enc.morse('-- --- .-. ... .') == 'MORSE'
    assert enc.morse('--/---/.-./.../.') == 'MORSE'


def test_semaphore():
    assert enc.semaphore('87 92 43 78') == 'TEST'
    assert enc.semaphore('78 29 34 87') == 'TEST'


def test_scrabble():
    assert enc.scrabble('QI') == 11
    assert enc.scrabble('all tiles are one!') == 14
