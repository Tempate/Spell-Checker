from .Soundex import Soundex
from .SpeedCop import SpeedCop

from fastDamerauLevenshtein import damerauLevenshtein
from collections import Counter
import re


class Corrector:
    def __init__(self, corpus):
        self.corpus = corpus
        self.corpus_length = sum(self.corpus.values())

        self.soundex_table = Soundex().gen_table(self.corpus.keys())

        self.scop = SpeedCop()
        self.scop_table, self.scop_keys = self.scop.gen_table(self.corpus.keys())

    def correct(self, word):
        suggestion = max(self.candidates(word.lower()), key=self.likelihood)
        return suggestion.title() if word[0].isupper() else suggestion

    def candidates(self, word):
        if word in self.corpus:
            return [word]

        # Find typing errors that are an edit away 
        close = self.scop.similar(self.scop_table, self.scop_keys, word, 20)

        if close := self.inbounds(word, close, 1):
            return close

        # Words that are one edit away
        edits = self.edit([word])

        if edits_known := self.known(edits):
            return edits_known

        # We check to see if there are similar-sounding 
        # words that are not too different
        if similar := self.inbounds(word, self.soundex(word), 2):
            return similar

        # Words that are two edits away
        reedits = self.edit(edits)

        if reedits_known := self.known(reedits):
            return reedits_known

        return [word]

    def likelihood(self, word): 
        # Percentage of times `word` appears in the text.
        return self.corpus[word] / self.corpus_length

    def soundex(self, word):
        # Find words that sound alike.
        code = Soundex.gen_code(word)

        try:
            return self.soundex_table[code]
        except KeyError:
            return []

    def known(self, words): 
        # The subset of `words` that appear in the corpus.
        return words & self.corpus.keys()

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

    def inbounds(self, target, words, limit):
        new_words = set()

        for word in words:
            dist = damerauLevenshtein(target, word, similarity=False)

            if dist <= limit:
                new_words.add(word)

        return new_words
