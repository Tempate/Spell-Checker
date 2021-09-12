import time


TEST_FILENAMES_WITHOUT_CONTEXT = [
    "tests/without_context/test1.txt",
    "tests/without_context/test2.txt",
    "tests/without_context/test3.txt"
]

TEST_FILENAMES_WITH_CONTEXT = [
    "tests/with_context/test1.txt"
]


class Tester:
    def __init__(self, corrector, verbose):
        self.correct = corrector.correct
        self.verbose = verbose

    def run(self):
        self.unit_tests()

        """
        for filename in TEST_FILENAMES_WITHOUT_CONTEXT:
            self.spell_test(self.parse(filename, False), False)
        """

        for filename in TEST_FILENAMES_WITH_CONTEXT:
            self.spell_test(self.parse(filename, True), True)

    def unit_tests(self):
        assert self.correct('speling') == 'spelling'              # insert
        assert self.correct('korrectud') == 'corrected'           # replace 2
        assert self.correct('bycycle') == 'bicycle'               # replace
        assert self.correct('inconvient') == 'inconvenient'       # insert 2
        assert self.correct('arrainged') == 'arranged'            # delete
        assert self.correct('peotry') =='poetry'                  # transpose
        assert self.correct('peotryy') =='poetry'                 # transpose + delete
        assert self.correct('word') == 'word'                     # known
        assert self.correct('quintessential') == 'quintessential' # unknown

    def spell_test(self, tests, with_context):
        # Run the spell correct on all (right, wrong) pairs.
        start = time.time()
        correct, unknown = 0, 0

        for right, wrong in tests:
            corrected = self.correct(wrong, with_context)
            
            if corrected == right:
                correct += 1
                
            elif self.verbose:
                print('{} => {}; expected: {}'.format(wrong, corrected, right))

        duration = time.time() - start
        test_count = len(tests)

        print('{:.0%} out of {} corrected at {:.0f} words per second '
            .format(correct / test_count, test_count, test_count / duration))
    
    @staticmethod
    def parse(filename, with_context=False):
        tests = []
    
        with open(filename) as test_file:
            for test in test_file.read().splitlines():
                right, wrongs = test.split(': ')

                if with_context:
                    tests += [(right, wrongs)]
                else:
                    tests += [(right, wrong) for wrong in wrongs.split()]

        return tests