import time

TEST_FILENAMES = [
    "tests/test1.txt"
    # "tests/test2.txt"
]


class Tester:
    def __init__(self, checker, verbose):
        self.checker = checker
        self.verbose = verbose

    def run(self):
        self.unit_tests()

        for filename in TEST_FILENAMES:
            self.spell_test(self.parse(filename))

    def unit_tests(self):
        assert self.checker.correct('speling') == 'spelling'              # insert
        assert self.checker.correct('korrectud') == 'corrected'           # replace 2
        assert self.checker.correct('bycycle') == 'bicycle'               # replace
        assert self.checker.correct('inconvient') == 'inconvenient'       # insert 2
        assert self.checker.correct('arrainged') == 'arranged'            # delete
        assert self.checker.correct('peotry') =='poetry'                  # transpose
        assert self.checker.correct('peotryy') =='poetry'                 # transpose + delete
        assert self.checker.correct('word') == 'word'                     # known
        assert self.checker.correct('quintessential') == 'quintessential' # unknown

    def spell_test(self, tests):
        # Run the spell checker on all (right, wrong) pairs.
        start = time.time()
        correct, unknown = 0, 0

        for right, wrong in tests:
            word = self.checker.correct(wrong)
            
            if word == right:
                correct += 1
                
            elif self.verbose:
                print('correct({}) => {} ({}); expected {} ({})'.format(
                    wrong, word, self.checker.corpus[word], right, self.checker.corpus[right]
                ))

        duration = time.time() - start
        test_count = len(tests)

        print('{:.0%} out of {} corrected at {:.0f} words per second '
            .format(correct / test_count, test_count, test_count / duration))
    
    @staticmethod
    def parse(filename):
        tests = []
    
        with open(filename) as test_file:
            for test in test_file.read().splitlines():
                right, wrongs = test.split(': ')
                tests += [(right, wrong) for wrong in wrongs.split()]

        return tests