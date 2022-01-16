import pytest
from nexusmaker import Record
from nexusmaker import NexusMaker
from nexusmaker import NexusMakerAscertained
from nexusmaker import NexusMakerAscertainedWords


@pytest.fixture(scope='class')
def testdata():
    return [
        Record(Language="A", Word="eye", Item="", Cognacy="1"),
        Record(Language="A", Word="leg", Item="", Cognacy="1"),
        Record(Language="A", Word="arm", Item="", Cognacy="1"),
    
        Record(Language="B", Word="eye", Item="", Cognacy="1"),
        Record(Language="B", Word="leg", Item="", Cognacy="2"),
        Record(Language="B", Word="arm", Item="", Cognacy="2"),
    
        Record(Language="C", Word="eye", Item="", Cognacy="1"),
        # No Record for C 'leg'
        Record(Language="C", Word="arm", Item="", Cognacy="3"),

        Record(Language="D", Word="eye", Item="", Cognacy="1", Loan=True),
        Record(Language="D", Word="leg", Item="", Cognacy="1"),
        Record(Language="D", Word="leg", Item="", Cognacy="2"),
        Record(Language="D", Word="arm", Item="", Cognacy="2,3"),
    ]


@pytest.fixture(scope='class')
def nexusmaker(testdata):
    return NexusMaker(data=testdata)


@pytest.fixture(scope='class')
def nexusmakerasc(testdata):
    return NexusMakerAscertained(data=testdata)


@pytest.fixture(scope='class')
def nexusmakerascwords(testdata):
    return NexusMakerAscertainedWords(data=testdata)

