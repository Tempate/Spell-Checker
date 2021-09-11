class SpeedCop:
    def __init__(self, words):
        self.table = self.gen_table(words)
        self.table_keys = sorted(self.table.keys())

    def similar(self, word, bound):
        code = self.gen_code(word)

        keys = sorted(self.table_keys + [code])
        index = keys.index(code)
        
        neighbors_keys = keys[max(index-bound, 0):index+bound]
        neighbors = set()

        for key in neighbors_keys:
            try:
                neighbors.add(self.table[key])
            except KeyError:
                continue

        return neighbors

    def gen_table(self, words):
        table = {}

        for word in words:
            code = self.gen_code(word)
            table[code] = word

        return table

    @staticmethod
    def gen_code(word):
        if not word:
            return ""

        code = word[0]

        consonants = []
        vowels = []

        for letter in word:
            dest = vowels if letter in 'aeiou' else consonants

            if letter not in dest and letter != word[0]:
                dest.append(letter)

        code += "".join(consonants)
        code += "".join(vowels)
        
        return code