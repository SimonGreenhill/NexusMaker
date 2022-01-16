import pytest
from nexusmaker import NexusMaker, Record

#Fix Bug caused by lru_cache on ._is_missing_for_word that made unique
#sites occur as single ones in blocks of missing states.
def test_lru_cache():
    maker = NexusMaker(data=[
        Record(Language="A", Word="eye", Item="", Cognacy="1"),
        Record(Language="B", Word="eye", Item="", Cognacy="1"),
        Record(Language="C", Word="eye", Item="", Cognacy="2"),
        Record(Language="D", Word="eye", Item="", Cognacy="2"),
        Record(Language="E", Word="eye", Item="", Cognacy=""),
    ])
    
    assert ('eye', '1') in maker.cognates
    assert ('eye', '2') in maker.cognates
    assert ('eye', 'u_1') in maker.cognates

    assert sorted(maker.cognates[('eye', '1')]) == ['A', 'B']
    assert sorted(maker.cognates[('eye', '2')]) == ['C', 'D']
    assert sorted(maker.cognates[('eye', 'u_1')]) == ['E']
    
    assert maker._is_missing_for_word('E', 'eye') == False

    nex = maker.make()
    assert nex.data['eye_1'] == {
        'A': '1', 'B': '1',
        'C': '0', 'D': '0',
        'E': '0' # NOT '?'
    }
    assert nex.data['eye_2'] == {
        'A': '0', 'B': '0',
        'C': '1', 'D': '1',
        'E': '0' # NOT '?'
    }
    assert nex.data['eye_u_1'] == {
        'A': '0', 'B': '0',
        'C': '0', 'D': '0',
        'E': '1'
    }
        