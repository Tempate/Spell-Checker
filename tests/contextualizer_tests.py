def test_contextualizer(contextualizer):
    test_parse(contextualizer)
    test_ngrams(contextualizer)


def test_parse(contextualizer):
    assert contextualizer.parse('Hello. This is it') == [
        '<s>', 'hello', '</s>', '<s>', 'this', 'is', 'it', '</s>'
    ]

    assert contextualizer.parse('Frankly, ridiculous!') == [
        '<s>', 'frankly', 'ridiculous', '</s>'
    ]

    assert contextualizer.parse('Never give all the heart') == [
        '<s>', 'never', 'give', 'all', 'the', 'heart', '</s>'
    ]

    print('[+] Parse tests passed successfully')


def test_ngrams(contextualizer):
    assert contextualizer.ngrams(['do', 'not', 'do', 'it'], 1) == {
        'do': 2, 
        'not': 1, 
        'it': 1
    }
    
    assert contextualizer.ngrams(['This', 'is', 'it'], 2) == {
        ('This', 'is'): 1, 
        ('is', 'it'): 1
    }
    
    assert contextualizer.ngrams(['That', 'is', 'not', 'cool'], 3) == {
        ('That', 'is', 'not'): 1, 
        ('is', 'not', 'cool'): 1
    }

    print('[+] n-grams tests passed successfully')