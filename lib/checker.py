from collections import Counter
import re


class SpellChecker:
    def __init__(self, corpus):
        self.corpus = corpus
        self.corpus_length = sum(self.corpus.values())

    def correct(self, word): 
        "Most probable spelling correction for word."
        return max(self.grade(word), key=self.likelihood)

    def likelihood(self, word): 
        "Percentage of times `word` appears in the text."
        return self.corpus[word] / self.corpus_length

    def grade(self, word): 
        "Score possible spelling corrections for word."        
        if word in self.corpus:
            return [word]

        dist1 = self.edit([word])
        
        return self.known(dist1) or self.known(self.edit(dist1)) or [word]

    def known(self, words): 
        "The subset of `words` that appear in the corpus."
        return words & self.corpus.keys()

    @staticmethod
    def edit(words):
        "Generate all words that are one Damerau–Levenshtein distance away."
        new_words = set()

        for word in words:
            for i in range(len(word) + 1):
                # Split word in two
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

            words = new_words

        return words
