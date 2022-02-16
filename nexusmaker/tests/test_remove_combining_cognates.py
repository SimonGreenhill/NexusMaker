import pytest

from nexusmaker import NexusMaker, Record
from nexusmaker.tools import remove_combining_cognates
from nexusmaker.tests.test_NexusMaker import TestNexusMaker


class TestNexusMakerRemovedCombining(TestNexusMaker):
    @pytest.fixture
    def maker(self, nexusmaker):
        return remove_combining_cognates(nexusmaker, keep=1)

    # everything should be the same except for this:
    # Record(ID=12, Language="D", Parameter="arm", Item="", Cognacy="2,3"),
    # ... which will no longer be in arm_3
    def test_arm_3(self, nexus):
        cog = 'arm_3'
        assert nexus.data[cog]['A'] == '0'
        assert nexus.data[cog]['B'] == '0'
        assert nexus.data[cog]['C'] == '1'
        assert nexus.data[cog]['D'] == '0'  # CHANGED VALUE


@pytest.fixture
def combiningmaker():
    return NexusMaker(data=[
        Record(Language="A", Parameter="word1", Item="", Cognacy="1"),
        Record(Language="B", Parameter="word1", Item="", Cognacy="1,2,3"),
        Record(Language="C", Parameter="word1", Item="", Cognacy="1"),

        Record(Language="A", Parameter="word2", Item="", Cognacy="1,2"),
        Record(Language="B", Parameter="word2", Item="", Cognacy="1,2,3"),
        Record(Language="C", Parameter="word2", Item="", Cognacy="1,3"),
    ])


def test_combining_1(combiningmaker):
    maker = remove_combining_cognates(combiningmaker, keep=1)
    assert ('word1', '1') in maker.cognates
    assert ('word1', '2') not in maker.cognates
    assert ('word1', '3') not in maker.cognates

    assert ('word2', '1') in maker.cognates
    assert ('word2', '2') not in maker.cognates
    assert ('word2', '3') not in maker.cognates

    assert sorted(maker.cognates[('word1', '1')]) == ['A', 'B', 'C']
    assert sorted(maker.cognates[('word2', '1')]) == ['A', 'B', 'C']

    nexus = maker.make()
    assert nexus.data['word1_1']['A'] == '1'
    assert nexus.data['word1_1']['B'] == '1'
    assert nexus.data['word1_1']['C'] == '1'
    assert nexus.data['word2_1']['A'] == '1'
    assert nexus.data['word2_1']['B'] == '1'
    assert nexus.data['word2_1']['C'] == '1'

    assert len(nexus.data.keys()) == 2


def test_combining_2(combiningmaker):
    maker = remove_combining_cognates(combiningmaker, keep=2)

    assert ('word1', '1') in maker.cognates
    assert ('word1', '2') in maker.cognates
    assert ('word1', '3') not in maker.cognates

    assert ('word2', '1') in maker.cognates
    assert ('word2', '2') in maker.cognates
    assert ('word2', '3') in maker.cognates

    assert sorted(maker.cognates[('word1', '1')]) == ['A', 'B', 'C']
    assert sorted(maker.cognates[('word1', '2')]) == ['B']

    assert sorted(maker.cognates[('word2', '1')]) == ['A', 'B', 'C']
    assert sorted(maker.cognates[('word2', '2')]) == ['A', 'B']
    assert sorted(maker.cognates[('word2', '3')]) == ['C']

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

    assert nexus.data['word2_3']['A'] == '0'
    assert nexus.data['word2_3']['B'] == '0'
    assert nexus.data['word2_3']['C'] == '1'
    
    assert len(nexus.data.keys()) == 5

