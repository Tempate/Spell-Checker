from .Soundex import Soundex
from .SpeedCop import SpeedCop
from .Contextualizer import Contextualizer, SEPARATORS

from fastDamerauLevenshtein import damerauLevenshtein
from collections import Counter
import regex as re


class Dealer:
    def __init__(self, words):
        self.words = words

        self.soundex = Soundex(self.words)
        self.speedcop = SpeedCop(self.words)

    def candidates(self, word):
        if self.known(set([word])):
            return [word]

        # Find typing errors that are an edit away
        close = self.speedcop.similar(word, 50)

        if close := self.inbounds(word, close, 1):
            return close

        # Words that are one edit away
        edits = self.edit([word])

        if edits_known := self.known(edits):
            return edits_known

        # We check to see if there are similar-sounding 
        # words that are not too different
        if similar := self.inbounds(word, self.soundex.candidates(word), 2):
            return similar

        # Words that are two edits away
        reedits = self.edit(edits)

        if reedits_known := self.known(reedits):
            return reedits_known

        return [word]

    def known(self, words): 
        # The subset of `words` that appear in the corpus.
        return words & self.words

    @staticmethod
    def edit(words):
        # Words that are one Damerau–Levenshtein distance away.
        new_words = set()

        for word in words:
            for i in range(len(word) + 1):
                # Split the word in two
                L = word[:i]
                R = word[i:]

                if R:
                    new_words.add(L + R[1:]) # deletion

                if len(R) >= 2:
                    new_words.add(L + R[1] + R[0] + R[2:]) # transposition

                for char in 'abcdefghijklmnopqrstuvwxyz':
                    if R:
                        new_words.add(L + char + R[1:]) # replacement

                    new_words.add(L + char + R) # insertion

        return new_words

    @staticmethod
    def inbounds(target, words, limit):
        new_words = set()

        for word in words:
            dist = damerauLevenshtein(target, word, similarity=False)

            if dist <= limit:
                new_words.add(word)

        return new_words
