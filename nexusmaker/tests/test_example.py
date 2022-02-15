from nexusmaker import NexusMaker, Record

# language      cognate             = nexus
# Maori    		1                   = 10
# Maori    	 	<not cognate>       = // removed as already coded for word
# Samoan 		1                   = 10
# Tahiatian  	<not cognate>       = u1 
# Tahiatian  	<not cognate>       = // removed as already coded for word 
# Tahiatian  	<not cognate>       = // removed as already coded for word
# Tongan    	<no data>           = ??  // missing data

def test_exampled():
    maker = NexusMaker(data=[
        Record(Language="Maori", Parameter="word1", Item="", Cognacy="1"),
        Record(Language="Maori", Parameter="word1", Item="", Cognacy=""),
        Record(Language="Samoan", Parameter="word1", Item="", Cognacy="1"),
        Record(Language="Tahitian", Parameter="word1", Item="", Cognacy=""),
        Record(Language="Tahitian", Parameter="word1", Item="", Cognacy=""),
        Record(Language="Tahitian", Parameter="word1", Item="", Cognacy=""),
        # ...note missing Tongan entry here.

        # add some entries for word 2 so Tongan will show as missing
        Record(Language="Tongan", Parameter="word2", Item="", Cognacy="1"),

    ])

    assert ('word1', '1') in maker.cognates
    assert ('word2', '1') in maker.cognates

    uniques = [c for c in maker.cognates if c[0] == 'word1' and c[1].startswith('u_')]
    assert len(uniques) == 1
    assert sorted(maker.cognates[('word1', '1')]) == ['Maori', 'Samoan']
    assert sorted(maker.cognates[uniques[0]]) == ['Tahitian']
    assert sorted(maker.cognates[('word2', '1')]) == ['Tongan']

    assert maker._is_missing_for_parameter('Tongan', 'word1') == True

    nex = maker.make()
    assert nex.data['word1_1'] == {
        'Maori':    '1',
        'Samoan':   '1',
        'Tahitian': '0',
        'Tongan':   '?',
    }

    assert nex.data["_".join(uniques[0])] == {
        'Maori':    '0',
        'Samoan':   '0',
        'Tahitian': '1',
        'Tongan':   '?',
    }
    
    assert nex.data['word2_1'] == {
        'Maori':    '?',
        'Samoan':   '?',
        'Tahitian': '?',
        'Tongan':   '1',
    }