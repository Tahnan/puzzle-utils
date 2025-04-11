from puzzle_utils import codes

SAMPLE_TEXT = 'This is an example.'


def test_atbash():
    atbash = codes.Atbash()
    assert atbash.encode(SAMPLE_TEXT) == 'Gsrh rh zm vcznkov.'
    assert atbash.decode(SAMPLE_TEXT) == atbash.encode(SAMPLE_TEXT)


def test_caesar():
    shift_one = 'Uijt jt bo fybnqmf.'
    caesar = codes.Caesar()
    assert caesar.encode(SAMPLE_TEXT, 1) == shift_one
    assert caesar.decode(shift_one, 1) == SAMPLE_TEXT
    assert caesar.encode(SAMPLE_TEXT, 27) == shift_one
    assert caesar.encode(SAMPLE_TEXT, 13) == caesar.decode(SAMPLE_TEXT, 13)

    all_shifts = caesar.show_all(SAMPLE_TEXT)
    assert all_shifts[0] == SAMPLE_TEXT
    assert all_shifts[1] == shift_one
    decoded = {caesar.decode(x, i) for i, x in enumerate(all_shifts)}
    assert decoded == {SAMPLE_TEXT}


def test_playfair():
    # Example taken from Wikipedia, which is easier than devising an example
    # from scratch that exercises all the cases.  But with a J added and an
    # odd number of letters.
    playfair = codes.Playfair('playfair example')
    ciphertext = playfair.encode('Just hide the gold in the tree stumps.')
    assert ciphertext == 'RTKZBMODZBXDNABEKUDMUIXMMOUVIFQM'
    plaintext = playfair.decode(ciphertext)
    assert plaintext == 'IUSTHIDETHEGOLDINTHETREXESTUMPSX'
