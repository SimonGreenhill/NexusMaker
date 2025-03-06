import pytest

from nexusmaker import NexusMaker, Record
from nexusmaker.tools import remove_combining_cognates


@pytest.fixture
def combiningmaker():
    return NexusMaker(data=[
        Record(Language="A", Parameter="word1", Item="", Cognacy="1"),
        Record(Language="B", Parameter="word1", Item="", Cognacy="1,2,3"),
        Record(Language="C", Parameter="word1", Item="", Cognacy="1"),

        Record(Language="A", Parameter="word2", Item="", Cognacy="1,2"),
        Record(Language="B", Parameter="word2", Item="", Cognacy="1,2,3"),
        Record(Language="C", Parameter="word2", Item="", Cognacy="1"),
    ])


def test_combining_1(combiningmaker):
    maker = remove_combining_cognates(combiningmaker, keep=1)
    
    # cognate sets that should be kept
    assert ('word1', '1') in maker.cognates

    assert ('word2', '1') in maker.cognates
    
    # cognate sets that should be removed
    assert ('word1', '2') not in maker.cognates
    assert ('word1', '3') not in maker.cognates

    assert ('word2', '2') not in maker.cognates
    assert ('word2', '3') not in maker.cognates
    
    # all taxa have membership of word1:1 and word2:1
    assert sorted(maker.cognates[('word1', '1')]) == ['A', 'B', 'C']
    assert sorted(maker.cognates[('word2', '1')]) == ['A', 'B', 'C']

    # check nexus file
    nexus = maker.make()
    assert nexus.data['word1_1']['A'] == '1'
    assert nexus.data['word1_1']['B'] == '1'
    assert nexus.data['word1_1']['C'] == '1'
    assert nexus.data['word2_1']['A'] == '1'
    assert nexus.data['word2_1']['B'] == '1'
    assert nexus.data['word2_1']['C'] == '1'

    # only two words
    assert len(nexus.data.keys()) == 2


def test_combining_2(combiningmaker):
    maker = remove_combining_cognates(combiningmaker, keep=2)
    
    # cognate sets that should be kept
    assert ('word1', '1') in maker.cognates
    assert ('word1', '2') in maker.cognates

    assert ('word2', '1') in maker.cognates
    assert ('word2', '2') in maker.cognates

    # cognate sets that should be removed
    assert ('word1', '3') not in maker.cognates
    assert ('word2', '3') not in maker.cognates
    
    # all taxa have membership of word1:1 and word2:1
    assert sorted(maker.cognates[('word1', '1')]) == ['A', 'B', 'C']
    assert sorted(maker.cognates[('word2', '1')]) == ['A', 'B', 'C']
    
    # ...but only B is word1:2
    assert sorted(maker.cognates[('word1', '2')]) == ['B']
    # ... and only A & C is word2:2
    assert sorted(maker.cognates[('word2', '2')]) == ['A', 'B']

    nexus = maker.make()
    
    assert nexus.data['word1_1']['A'] == '1'
    assert nexus.data['word1_1']['B'] == '1'
    assert nexus.data['word1_1']['C'] == '1'

    assert nexus.data['word1_2']['A'] == '0'
    assert nexus.data['word1_2']['B'] == '1'
    assert nexus.data['word1_2']['C'] == '0'

    assert nexus.data['word2_1']['A'] == '1'
    assert nexus.data['word2_1']['B'] == '1'
    assert nexus.data['word2_1']['C'] == '1'

    assert nexus.data['word2_2']['A'] == '1'
    assert nexus.data['word2_2']['B'] == '1'
    assert nexus.data['word2_2']['C'] == '0'

    assert len(nexus.data.keys()) == 4
