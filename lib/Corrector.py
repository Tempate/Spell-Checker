
from .Contextualizer import Contextualizer, SEPARATORS
from .Dealer import Dealer

import regex as re


class Corrector:
    def __init__(self, corpus):
        self.contextualizer = Contextualizer(corpus)
        self.dealer = Dealer(self.contextualizer.words)

    def correct(self, text, use_context=False):
        if use_context:
            self.context = ['</s>'] + self.contextualizer.parse(text)
        
        correction = lambda m: self.correct_word(m.group(), use_context)
        return re.sub('\p{L}+', correction, text)

    def correct_word(self, word, use_context=False):
        if use_context:
            suggestion = max(self.dealer.candidates(word.lower()), key=self.likelihood)

            # Adjust context for the next word
            self.context = self.context[1:]

            while len(self.context) >= 3 and self.context[2] in SEPARATORS:        
                self.context = self.context[1:]

        else:
            suggestion = max(self.dealer.candidates(word.lower()), key=self.contextualizer.frequency)

        # Keep capitalization
        if word[0].isupper():
            return suggestion.title()

        return suggestion

    def likelihood(self, word): 
        return self.contextualizer.prob_word_is_right(word, self.context[:2])
