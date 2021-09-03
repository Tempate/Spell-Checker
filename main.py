from lib.Corrector import Corrector
from test import Tester

from optparse import OptionParser
from collections import Counter

import re


CORPUS = "corpus.txt"


def main():
    options = read_commands()
    corrector = Corrector(options.corpus)

    if options.test:
        Tester(corrector, options.verbose).run()
        exit(0)

    if options.output:
        output = open(options.output, 'w')

    for word in options.input:
        suggestion = corrector.correct(word)

        if options.output:
            output.write(suggestion + ' ')
        else:
            print(suggestion)

    if options.output:
        output.write("\n")
        output.close()


def read_commands():
    parser = OptionParser("%prog -f <input_file>")
    parser.add_option("-f", dest="input", help="File to correct")
    parser.add_option("-o", dest="output", help="File to save the corrections")
    parser.add_option("-c", dest="corpus", help="Corpus in a txt file")
    parser.add_option("-t", action="store_true", default=False, dest="test", help="Run tests")
    parser.add_option("-v", action="store_true", default=False, dest="verbose", help="Make the output verbose")

    (options, args) = parser.parse_args()

    with open(options.corpus or CORPUS) as corpus:
        words = re.findall(r'\w+', corpus.read().lower())
        options.corpus = Counter(words)

    if options.input:
        with open(options.input) as f:
            options.input = f.read().splitlines()
    elif not options.test:
        options.input = input().split()

    return options


if __name__ == "__main__":
    main()
