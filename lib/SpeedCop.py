class SpeedCop:
    def __init__(self, words):
        self.table = self.gen_table(words)
        self.table_keys = list(self.table.keys())

    def similar(self, word, bound):
        code = self.gen_code(word)

        # Find the 2*bound closest codes
        codes = sorted(set(self.table_keys + [code]))
        index = codes.index(code)
        
        neighbors_codes = codes[max(index-bound, 0):index+bound]
        neighbors = set()

        for code in neighbors_codes:
            try:
                neighbors.add(self.table[code])
            except KeyError:
                continue

        return neighbors

    def gen_table(self, words):
        table = {}

        for word in words:
            table[self.gen_code(word)] = word

        return table

    @staticmethod
    def gen_code(word):
        if not word:
            return ""

        code = word[0]

        vowels = ''

        for letter in word:
            dest = vowels if letter in 'aeiou' else code

            if letter not in dest and letter != word[0]:
                dest += letter

        code += vowels
        
        return code