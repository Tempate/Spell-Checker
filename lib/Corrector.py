from .Soundex import Soundex

from collections import Counter
import re


class Corrector:
    def __init__(self, corpus):
        self.corpus = corpus
        self.corpus_length = sum(self.corpus.values())

        self.soundex_table = Soundex().gen_table(self.corpus.keys())

    def correct(self, word): 
        return max(self.candidates(word), key=self.likelihood)

    def candidates(self, word):       
        if word in self.corpus:
            return [word]

        # Words that are one edit away
        edits = self.edit([word])

        if edits_known := self.known(edits):
            return edits_known

        # We check to see if there are similar-sounding words
        # that are not too different
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
            dist = self.distance(target, word)

            if dist <= limit:
                new_words.add(word)

        return new_words

    @staticmethod
    def distance(word1, word2):
        if word1 == word2:
            return 0

        lens = [len(word1), len(word2)]
        dist = max(lens) - min(lens)

        for i in range(min(lens)):
            dist += word1[i] != word2[i]

        return dist
