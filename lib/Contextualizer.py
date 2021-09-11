import regex as re


SEPARATORS = ['<s>', '</s>']


class Contextualizer:
    def __init__(self, corpus):
        self.tokens = self.parse(corpus)
        self.words = set([token for token in self.tokens if token not in SEPARATORS])

        self.unigrams = self.ngrams(self.tokens, 1) 
        self.bigrams  = self.ngrams(self.tokens, 2)
        self.trigrams = self.ngrams(self.tokens, 3)

    def parse(self, text):
        # 'Hello. This is it.' => ['<s>', 'hello', '</s>', '<s>', 'this', 'is', 'it', '</s>']
        return re.split('\s|\n', self.segment_sentences(text))

    def prob_word_is_right(self, word, context):
        try:
            if context[-1] == '<s>':
                # Probability that word starts a sentence
                return self.bigrams[('<s>', word)] / self.frequency('<s>')

            bigram = tuple(context[-2:])
            return self.trigrams[(*bigram, word)] / self.bigrams[bigram]
        except KeyError:
            return 0

    def frequency(self, word):
        try:
            return self.unigrams[word]
        except KeyError:
            return 0

    @staticmethod
    def ngrams(words, n): 
        ngrams_freq = {}
        
        for i in range(len(words) - (n-1)):
            if n == 1:
                ngram = words[i]
            else:
                ngram = tuple(words[i:i+n])

            try:
                ngrams_freq[ngram] += 1
            except KeyError:
                ngrams_freq[ngram] = 1
        
        return ngrams_freq

    @staticmethod
    def segment_sentences(text):
        # Replace weird symbols with a space
        text = re.sub('[^\p{L}\.;:?!]+', ' ', text)

        # Add markup to indicate to separate sentences
        sentence_boundaries = '[\.;:?!]+\p{Zs}+(\p{Lu})'
        sentence_markup = r' </s>\n<s> \1'

        text = '<s> ' + re.sub(sentence_boundaries, sentence_markup, text) + ' </s>'

        # Remove duplicate spaces and punctuation signs
        text = re.sub('\p{Zs}{2,}', ' ', text)
        text = re.sub('[\.;:?!]', '', text)
        
        return text.lower()