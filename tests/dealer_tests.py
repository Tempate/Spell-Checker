def test_dealer(dealer):
    test_candidates(dealer)
    test_editor(dealer)
    test_known(dealer)


def test_candidates(dealer):
    assert 'where' in dealer.candidates('whre')
    assert 'were'  in dealer.candidates('whre')
    assert 'car'   in dealer.candidates('carr')
    assert 'care'  in dealer.candidates('carr')
    assert 'carry' in dealer.candidates('carr')
    assert 'funny' in dealer.candidates('funn')
    assert 'fun'   in dealer.candidates('funn')

    print('[+] Candidates tests passed successfully')


def test_editor(dealer):
    assert 'bhey'  in dealer.edit(['hey'])
    assert 'hrey'  in dealer.edit(['hey'])
    assert 'hely'  in dealer.edit(['hey'])
    assert 'heyt'  in dealer.edit(['hey'])
    assert 'ove'   in dealer.edit(['love'])
    assert 'lve'   in dealer.edit(['love'])
    assert 'loe'   in dealer.edit(['love'])
    assert 'lov'   in dealer.edit(['love'])
    assert 'thip'  in dealer.edit(['chip'])
    assert 'cmip'  in dealer.edit(['chip'])
    assert 'chtp'  in dealer.edit(['chip'])
    assert 'chia'  in dealer.edit(['chip'])
    assert 'awgon' in dealer.edit(['wagon'])
    assert 'wgaon' in dealer.edit(['wagon'])
    assert 'waogn' in dealer.edit(['wagon'])
    assert 'wagno' in dealer.edit(['wagon'])

    print('[+] Editor tests passed successfully')


def test_known(dealer):
    assert dealer.known(set(['word']))
    assert dealer.known(set(['rat']))
    assert dealer.known(set(['field']))
    assert dealer.known(set(['moon']))
    assert dealer.known(set(['park']))

    assert not dealer.known(set(['piasd']))
    assert not dealer.known(set(['golatr']))
    assert not dealer.known(set(['pogeta']))
    assert not dealer.known(set(['ricogado']))

    print('[+] Known tests passed successfully') 
