import sys
import unittest

from nexusmaker import NexusMaker, NexusMakerAscertained, NexusMakerAscertainedWords, Record

TESTDATA = [
    Record(language="A", word="eye", item="", cognate="1"),
    Record(language="A", word="leg", item="", cognate="1"),
    Record(language="A", word="arm", item="", cognate="1"),
    
    Record(language="B", word="eye", item="", cognate="1"),
    Record(language="B", word="leg", item="", cognate="2"),
    Record(language="B", word="arm", item="", cognate="2"),
    
    Record(language="C", word="eye", item="", cognate="1"),
    # No Record for C 'leg'
    Record(language="C", word="arm", item="", cognate="3"),

    Record(language="D", word="eye", item="", cognate="1", loan=True),
    Record(language="D", word="leg", item="", cognate="1"),
    Record(language="D", word="leg", item="", cognate="2"),
    Record(language="D", word="arm", item="", cognate="2,3"),
]


class TestNexusMakerInternals(unittest.TestCase):
    def test_error_on_non_record(self):
        with self.assertRaises(ValueError):
            NexusMaker(['1'])
        with self.assertRaises(ValueError):
            NexusMaker([('a', 'tuple', 'of', 'stuff')])
    
    def test_can_still_subclass_record(self):
        class R2(Record):
            pass
        NexusMaker([R2("")])



class TestNexusMaker(unittest.TestCase):
    model = NexusMaker
    
    def setUp(self):
        self.maker = self.model(data=TESTDATA)
        self.nex = self.maker.make()
    
    def test_languages(self):
        self.assertEqual(self.maker.languages, {'A', 'B', 'C', 'D'})
    
    def test_words(self):
        self.assertEqual(self.maker.words, {'eye', 'leg', 'arm'})
    
    def test_nsites(self):
        assert len(self.nex.data.keys()) == 6
    
    def test_cognates(self):
        assert ('eye', '1') in self.maker.cognates.keys()
        assert ('leg', '1') in self.maker.cognates.keys()
        assert ('leg', '2') in self.maker.cognates.keys()
        assert ('arm', '1') in self.maker.cognates.keys()
        assert ('arm', '2') in self.maker.cognates.keys()
        assert ('arm', '3') in self.maker.cognates.keys()
    
    def test_is_missing_for_word(self):
        assert self.maker._is_missing_for_word('A', 'eye') == False
        assert self.maker._is_missing_for_word('A', 'leg') == False
        assert self.maker._is_missing_for_word('A', 'arm') == False
        
        assert self.maker._is_missing_for_word('B', 'eye') == False
        assert self.maker._is_missing_for_word('B', 'leg') == False
        assert self.maker._is_missing_for_word('B', 'arm') == False

        assert self.maker._is_missing_for_word('C', 'eye') == False
        assert self.maker._is_missing_for_word('C', 'leg') == True, "Should be missing 'leg' for language 'C'"
        assert self.maker._is_missing_for_word('C', 'arm') == False

        assert self.maker._is_missing_for_word('D', 'eye') == True, "Should be missing 'eye' for language 'D' (loan)"
        assert self.maker._is_missing_for_word('D', 'leg') == False
        assert self.maker._is_missing_for_word('D', 'arm') == False
        
    def test_eye_1(self):
        cog = 'eye_1'
        assert self.nex.data[cog]['A'] == '1'
        assert self.nex.data[cog]['B'] == '1'
        assert self.nex.data[cog]['C'] == '1'
        assert self.nex.data[cog]['D'] == '?'
        
    def test_leg_1(self):
        cog = 'leg_1'
        assert self.nex.data[cog]['A'] == '1'
        assert self.nex.data[cog]['B'] == '0'
        assert self.nex.data[cog]['C'] == '?'
        assert self.nex.data[cog]['D'] == '1'

    def test_leg_2(self):
        cog = 'leg_2'
        assert self.nex.data[cog]['A'] == '0'
        assert self.nex.data[cog]['B'] == '1'
        assert self.nex.data[cog]['C'] == '?'
        assert self.nex.data[cog]['D'] == '1'

    def test_arm_1(self):
        cog = 'arm_1'
        assert self.nex.data[cog]['A'] == '1'
        assert self.nex.data[cog]['B'] == '0'
        assert self.nex.data[cog]['C'] == '0'
        assert self.nex.data[cog]['D'] == '0'

    def test_arm_2(self):
        cog = 'arm_2'
        assert self.nex.data[cog]['A'] == '0'
        assert self.nex.data[cog]['B'] == '1'
        assert self.nex.data[cog]['C'] == '0'
        assert self.nex.data[cog]['D'] == '1'

    def test_arm_3(self):
        cog = 'arm_3'
        assert self.nex.data[cog]['A'] == '0'
        assert self.nex.data[cog]['B'] == '0'
        assert self.nex.data[cog]['C'] == '1'
        assert self.nex.data[cog]['D'] == '1'
    
    def test_write(self):
        out = self.maker.write()
        assert out.startswith("#NEXUS")
        assert 'NTAX=4' in out
        assert 'CHARSTATELABELS' in out
        assert 'MATRIX' in out


class TestNexusMakerAscertained(TestNexusMaker):
    model = NexusMakerAscertained
    
    # 1 more site than before in ascertainment = none
    def test_nsites(self):
        assert len(self.nex.data.keys()) == 7
    
    def test_ascertainment_column(self):
        assert self.maker.OVERALL_ASCERTAINMENT_LABEL in self.nex.data
        for k in self.nex.data[self.maker.OVERALL_ASCERTAINMENT_LABEL]:
            assert self.nex.data[self.maker.OVERALL_ASCERTAINMENT_LABEL][k] == '0'
    


if __name__ == '__main__':
    unittest.main()


