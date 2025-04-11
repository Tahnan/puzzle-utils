# puzzle_utils

This package is a set of utilities that I find useful for puzzles, both writing and solving. It's not intended to be comprehensive; it's not even *particularly* intended to be generalized. It's very much tailored to do what I need.

This README is a high-level overview of the contents.

## General utilities

The functions in `__init__.py` are general utility functions for things that come up a lot in puzzling: stripping strings of nonalphabetic characters, for instance, or getting the prime factors of a number.

## data

`puzzle_utils.data` contains dictionaries, particularly those that map letters to encoded versions (or vice versa) for common encodings like Braille, Morse code, and semaphore.

It also contains data on letter frequency and bigram frequency in English, useful for certain kinds of codebreaking.

## encodings

`puzzle_utils.encodings` has functions that use the data dictionaries, to e.g. convert Morse code to letters, or letters to their Scrabble score.

## anagrams

`puzzle_utils.anagrams` has functions and a subclass of `dict` that assist in working with anagrams, by converting letters to primes and words as the products of their letters.  (As noted in the file, this idea is not original to me.)

While the file doesn't demonstrate this, using numbers to represent words simplifies tasks like:
* determining whether one string is an anagram of another
  * two words are anagrams if their numbers are equal (that is, if `letters_to_primes(one) == letters_to_primes(two)`)
* determining whether one string is a *subanagram* of another, i.e. whether one word contains all the letters of another
  * Rather than something complicated involving Counter subtraction, modular arithmetic does the trick.  For instance, **EXAMPLE** is 109711060 (2 * 83 * 5 * 43 * 53 * 29 * 2, because **E** is 2, **X** is 83, etc.), and **MEGAPLEX** is 6472952540.  To determine that **EXAMPLE** is a subanagram of **MEGAPLEX**, we can check whether `6472952540 % 109711060 == 0` (which it does).
  * If we want the difference between a word and its subanagram, `divmod()` gives it (while checking that the latter is a subanagram).  `divmod(6472952540, 109711060) == (59, 0)`, telling us that **EXAMPLE** is a subanagram (because the remainder is 0) and that the difference between the two words is `59` (which `primes_to_letters` tells us is `G`).
  
## grid

A lot of puzzles involve grids (often of letters, though see also the maze traversal that often appears in Advent of Code problems).  Representing a grid as a dictionary from coordinates to the letter at those coordinates (or wall/floor, etc.) allows both easy lookup of a particular spot in the grid and other retrieval functions.

The heart of `puzzle_utils.grid` is the `Grid` class, a dictionary that defines additional methods for getting information like the contents of a row or column, or the neighbors of a space in the grid.  It also independently defines functions for moving in a given direction from a coordinate and for turning to a new direction.

## codes

`codes` contains classes to handle some common ciphers: Atbash, Caesar shifts, and Playfair.
