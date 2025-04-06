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