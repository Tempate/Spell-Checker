CODES = {
    'b': 1, 'f': 1, 'p': 1, 'v': 1,
    'c': 2, 'g': 2, 'j': 2, 'k': 2, 'q': 2, 's': 2, 'x': 2, 'z': 2,
    'd': 3, 't': 3,
    'l': 4,
    'm': 5, 'n': 5,
    'r': 6
}

CODE_LENGTH = 4

class Soundex:
    def gen_table(self, words):
        table = {}

        for word in words:
            code = self.gen_code(word)

            if code not in table:
                table[code] = [word]
            else:
                table[code] += [word]

        return table


    @staticmethod
    def gen_code(word):
        # A slightly-different (the first letter is also encoded) 
        # implementation of the standard soundex coding algorithm.
        code = ""

        for letter in word:
            if letter in ['a', 'e', 'i', 'o', 'u', 'y', 'h', 'w']:
                continue

            if not letter.isalpha():
                continue
            
            if not code or code[-1] != CODES[letter]:
                code += str(CODES[letter])

        code = code[:CODE_LENGTH] # Limit the size of the code
        code += (CODE_LENGTH - len(code)) * '0' # Pad with zeros
        
        return code