import time

from tests.dealer_tests import test_dealer
from tests.contextualizer_tests import test_contextualizer


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
        self.corrector = corrector
        self.verbose = verbose

    def run(self):
        self.basic_tests()

        test_dealer(self.corrector.dealer)
        test_contextualizer(self.corrector.contextualizer)

        for filename in TEST_FILENAMES_WITHOUT_CONTEXT:
            self.corrector_test(self.parse(filename, False), False)

        for filename in TEST_FILENAMES_WITH_CONTEXT:
            self.corrector_test(self.parse(filename, True), True)

    def basic_tests(self):
        # simple
        assert self.corrector.correct('speling') == 'spelling'              # insert
        assert self.corrector.correct('arrainged') == 'arranged'            # delete
        assert self.corrector.correct('bycycle') == 'bicycle'               # replace
        assert self.corrector.correct('peotry') =='poetry'                  # transpose

        assert self.corrector.correct('word') == 'word'                     # known
        assert self.corrector.correct('quintessential') == 'quintessential' # unknown
        
        # double
        assert self.corrector.correct('inconvient') == 'inconvenient'       # insert
        assert self.corrector.correct('korrectud') == 'corrected'           # replace
        assert self.corrector.correct('peotryy') =='poetry'                 # transpose + delete

        print('[+] Basic tests passed successfully')
        
    def corrector_test(self, tests, with_context):
        # Run the corrector on all (right, wrong) pairs.
        start = time.time()
        correct, unknown = 0, 0

        for right, wrong in tests:
            corrected = self.corrector.correct(wrong, with_context)
            
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