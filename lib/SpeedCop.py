class SpeedCop:
    def similar(self, table, keys, word, bound):
        code = self.gen_code(word)

        keys.append(code)
        index = keys.index(code)
        
        neighbors_keys = keys[max(index-bound, 0):index+bound]
        neighbors = set()

        for key in neighbors_keys:
            try:
                neighbors.add(table[key])
            except KeyError:
                continue

        return neighbors

    def gen_table(self, words):
        table = {}
        keys = set()

        for word in words:
            code = self.gen_code(word)

            table[code] = word
            keys.add(code)

        return table, sorted(keys)

    @staticmethod
    def gen_code(word):
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