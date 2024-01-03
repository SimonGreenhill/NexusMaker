from nexusmaker import NexusMaker, Record

def test_tng():
    maker = NexusMaker(data=[
        Record(ID=1, Language="kuman", Parameter="1035_GOOD", Item="wagai", Cognacy=19),
        Record(ID=2, Language="kuman", Parameter="1035_GOOD", Item="wəlaŋ", Cognacy=10),
        Record(ID=3, Language="sikalan", Parameter="1035_GOOD", Item="kɨndəm", Cognacy=43),
        Record(ID=4, Language="sokan", Parameter="1035_GOOD", Item="wəlaŋ", Cognacy=10),
        Record(ID=5, Language="dzenzen", Parameter="1035_GOOD", Item="qɑdɛm", Cognacy=43),

        Record(ID=6, Language="dzenzen", Parameter="1036_BAD", Item="xxx", Cognacy=1),
        Record(ID=6, Language="sokan", Parameter="1036_BAD", Item="xxx", Cognacy=""),
    ])

    assert ('1035_GOOD', '10') in maker.cognates
    assert ('1035_GOOD', '19') in maker.cognates
    assert ('1035_GOOD', '43') in maker.cognates
    assert ('1036_BAD', '1') in maker.cognates

    assert sorted(maker.cognates[('1035_GOOD', '10')]) == ['kuman', 'sokan']
    assert sorted(maker.cognates[('1035_GOOD', '19')]) == ['kuman']
    assert sorted(maker.cognates[('1035_GOOD', '43')]) == ['dzenzen', 'sikalan']
    assert sorted(maker.cognates[('1036_BAD', '1')]) == ['dzenzen']

    assert maker._is_missing_for_parameter('kuman', '1036_BAD')
    assert maker._is_missing_for_parameter('sikalan', '1036_BAD')

    nex = maker.make()
    
    assert nex.data['1035good_10'] == {
        'kuman':    '1',
        'sokan':    '1',
        'sikalan':  '0',
        'dzenzen':  '0',
    }

    assert nex.data['1035good_19'] == {
        'kuman':    '1',
        'sokan':    '0',
        'sikalan':  '0',
        'dzenzen':  '0',
    }

    assert nex.data['1035good_43'] == {
        'kuman':    '0',
        'sokan':    '0',
        'sikalan':  '1',
        'dzenzen':  '1',
    }

    assert nex.data['1036bad_1'] == {
        'kuman':    '?',
        'sokan':    '0',
        'sikalan':  '?',
        'dzenzen':  '1',
    }
    
    # and a unique from sokan
    assert nex.data['1036bad_u_1'] == {
        'kuman':    '?',
        'sokan':    '1',
        'sikalan':  '?',
        'dzenzen':  '0',
    }
