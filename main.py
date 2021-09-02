from lib.checker import SpellChecker
from test import Tester

from optparse import OptionParser
from collections import Counter

import re


CORPUS = "corpus.txt"


def main():
    options = read_commands()
    checker = SpellChecker(options.corpus)

    if options.test:
        tester = Tester(checker, options.verbose)
        tester.run()
    else:
        output = open(options.output, 'w')

        for word in options.input:
            output.write(checker.correct(word) + " ")

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
        options.input = input("Text to analyse: ").split()

    if not options.output:
        options.output = "corrected.txt"

    return options


if __name__ == "__main__":
    main()